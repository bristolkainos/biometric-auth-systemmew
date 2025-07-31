import json
import os
from web3 import Web3
import logging


logger = logging.getLogger(__name__)


class BlockchainService:
    def __init__(self):
        # Blockchain configuration
        self.w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
        
        # Contract configuration
        self.contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
        
        # Load contract ABI
        abi_path = os.path.join(os.path.dirname(__file__), '..', '..', 'contract_abi.json')
        with open(abi_path, 'r') as f:
            contract_abi = json.load(f)
        
        self.contract = self.w3.eth.contract(
            address=self.w3.to_checksum_address(self.contract_address),
            abi=contract_abi
        )
        
        # Use the first account from Hardhat as the owner
        self.owner_address = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
        self.owner_private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
        
        # Check if blockchain is connected
        try:
            if not self.w3.is_connected():
                logger.warning("Blockchain connection failed. Blockchain features will be disabled.")
                self.enabled = False
            else:
                logger.info(f"Connected to blockchain successfully")
                logger.info(f"Contract address: {self.contract_address}")
                self.enabled = True
        except Exception as e:
            logger.warning(f"Blockchain connection failed: {e}. Blockchain features will be disabled.")
            self.enabled = False

    def mint_biometric_token(self, user_address, user_id, biometric_hash, biometric_type, token_uri=""):
        """
        Mint a new biometric token (NFT) on the blockchain
        """
        if not self.enabled:
            logger.warning("Blockchain is not enabled. Skipping token minting.")
            return None
            
        try:
            # Prepare transaction
            nonce = self.w3.eth.get_transaction_count(self.w3.to_checksum_address(self.owner_address))
            
            # Build transaction
            transaction = self.contract.functions.mintBiometricToken(
                user_address,
                user_id,
                biometric_hash,
                biometric_type,
                token_uri
            ).build_transaction({
                'from': self.owner_address,
                'nonce': nonce,
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            # Sign transaction
            signed_txn = self.w3.eth.account.sign_transaction(
                transaction, 
                self.owner_private_key
            )
            
            # Send transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # Wait for transaction receipt
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            # Get token ID from event
            token_id = None
            for log in tx_receipt['logs']:
                try:
                    decoded_log = self.contract.events.BiometricTokenMinted().process_log(log)
                    token_id = decoded_log['args']['tokenId']
                    break
                except:
                    continue
            
            if token_id is None:
                # Fallback: get the next token ID
                token_id = self.contract.functions.nextTokenId().call() - 1
            
            logger.info(f"Successfully minted biometric token {token_id} for user {user_id}")
            
            return {
                'token_id': token_id,
                'transaction_hash': tx_hash.hex(),
                'block_number': tx_receipt['blockNumber'],
                'user_address': user_address,
                'user_id': user_id,
                'biometric_type': biometric_type
            }
            
        except Exception as e:
            logger.error(f"Error minting biometric token: {e}")
            return None

    def get_biometric_data(self, token_id):
        """
        Get biometric data for a specific token
        """
        if not self.enabled:
            logger.warning("Blockchain is not enabled. Cannot retrieve token data.")
            return None
            
        try:
            user_id, biometric_hash, biometric_type = self.contract.functions.getBiometricData(token_id).call()
            return {
                'token_id': token_id,
                'user_id': user_id,
                'biometric_hash': biometric_hash,
                'biometric_type': biometric_type
            }
        except Exception as e:
            logger.error(f"Error getting biometric data for token {token_id}: {e}")
            return None

    def get_user_tokens(self, user_id):
        """
        Get all tokens for a specific user
        """
        if not self.enabled:
            logger.warning("Blockchain is not enabled. Cannot retrieve user tokens.")
            return []
            
        try:
            token_ids = self.contract.functions.getTokensByUser(user_id).call()
            return [int(token_id) for token_id in token_ids]
        except Exception as e:
            logger.error(f"Error getting tokens for user {user_id}: {e}")
            return []

    def record_login_event(self, user_id, login_timestamp):
        """
        Record a login event on the blockchain (optional feature)
        """
        if not self.enabled:
            logger.warning("Blockchain is not enabled. Skipping login event recording.")
            return None
            
        try:
            # This could be implemented as a separate event or stored in a different contract
            # For now, we'll just log it
            logger.info(f"Login event recorded for user {user_id} at {login_timestamp}")
            return "login_event_recorded"
        except Exception as e:
            logger.error(f"Error recording login event: {e}")
            return None


# Global instance
blockchain_service = BlockchainService() 
