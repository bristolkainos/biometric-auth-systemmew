#!/usr/bin/env python3
"""
Script to regenerate biometric analysis data for all existing biometric records.
This ensures admin dashboard shows real analysis instead of mock data.
"""

import sys
import os
sys.path.append('.')

# Import with absolute path
from core.database import SessionLocal
from biometric_data import BiometricData
from biometric_service import BiometricService
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def regenerate_all_biometric_analysis():
    """Regenerate biometric analysis for all records that don't have it"""
    db = SessionLocal()
    try:
        # Initialize biometric service
        biometric_service = BiometricService()
        biometric_service.initialize()
        
        # Find all biometric records without analysis
        unprocessed_records = db.query(BiometricData).filter(
            BiometricData.processing_analysis.is_(None)
        ).all()
        
        logger.info(f"Found {len(unprocessed_records)} records without analysis")
        
        processed_count = 0
        failed_count = 0
        
        for record in unprocessed_records:
            try:
                if record.image_data:
                    logger.info(f"Processing biometric record {record.id} ({record.biometric_type})")
                    
                    # Generate real biometric analysis
                    result = biometric_service.process_biometric_detailed(
                        record.image_data, 
                        record.biometric_type, 
                        record.user_id
                    )
                    
                    # Store the analysis
                    record.processing_analysis = json.dumps(result["detailed_analysis"])
                    processed_count += 1
                    
                    logger.info(f"✅ Successfully processed record {record.id}")
                else:
                    logger.warning(f"⚠️ Record {record.id} has no image data")
                    failed_count += 1
                    
            except Exception as e:
                logger.error(f"❌ Failed to process record {record.id}: {e}")
                failed_count += 1
                continue
        
        # Commit all changes
        try:
            db.commit()
            logger.info(f"✅ Successfully committed {processed_count} processed records")
        except Exception as e:
            db.rollback()
            logger.error(f"❌ Failed to commit changes: {e}")
            return False
            
        # Check records with existing analysis
        existing_analyzed = db.query(BiometricData).filter(
            BiometricData.processing_analysis.isnot(None)
        ).count()
        
        total_records = db.query(BiometricData).count()
        
        logger.info(f"""
📊 Biometric Analysis Regeneration Complete:
   - Total biometric records: {total_records}
   - Records with analysis: {existing_analyzed}
   - Newly processed: {processed_count}
   - Failed: {failed_count}
   - Coverage: {(existing_analyzed/total_records*100) if total_records > 0 else 0:.1f}%
        """)
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Unexpected error during regeneration: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    logger.info("🚀 Starting biometric analysis regeneration...")
    success = regenerate_all_biometric_analysis()
    
    if success:
        logger.info("✅ Biometric analysis regeneration completed successfully!")
        logger.info("Admin dashboard will now show real analysis data instead of test visualizations.")
    else:
        logger.error("❌ Biometric analysis regeneration failed!")
        sys.exit(1)
