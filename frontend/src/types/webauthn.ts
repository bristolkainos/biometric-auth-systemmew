// WebAuthn TypeScript interfaces for mobile biometric authentication

export interface WebAuthnCredential {
  id: string;
  rawId: ArrayBuffer;
  response: AuthenticatorAttestationResponse | AuthenticatorAssertionResponse;
  type: 'public-key';
}

export interface WebAuthnRegistrationData {
  id: string;
  rawId: number[];
  response: {
    attestationObject: number[];
    clientDataJSON: number[];
  };
  type: string;
}

export interface WebAuthnVerificationData {
  id: string;
  rawId: number[];
  response: {
    authenticatorData: number[];
    clientDataJSON: number[];
    signature: number[];
    userHandle?: number[];
  };
  type: string;
}

export interface MobileBiometricCapabilities {
  fingerprint: boolean;
  faceId: boolean;
  touchId: boolean;
  androidBiometric: boolean;
  windowsHello: boolean;
  linuxFingerprint: boolean;
  laptopBiometric: boolean;
}

export interface BiometricAuthOptions {
  challenge: ArrayBuffer;
  timeout: number;
  userVerification: 'required' | 'preferred' | 'discouraged';
  authenticatorSelection?: {
    authenticatorAttachment: 'platform' | 'cross-platform';
    userVerification: 'required' | 'preferred' | 'discouraged';
    requireResidentKey?: boolean;
  };
}

// Utility functions for mobile and laptop biometric detection
export const detectMobileBiometrics = async (): Promise<MobileBiometricCapabilities> => {
  const capabilities: MobileBiometricCapabilities = {
    fingerprint: false,
    faceId: false,
    touchId: false,
    androidBiometric: false,
    windowsHello: false,
    linuxFingerprint: false,
    laptopBiometric: false,
  };

  // Check if WebAuthn is available
  if (!window.PublicKeyCredential) {
    return capabilities;
  }

  try {
    // Check for platform authenticator (Touch ID, Face ID, Windows Hello, Android Biometric)
    const available = await PublicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable();
    
    if (available) {
      const userAgent = navigator.userAgent.toLowerCase();
      const platform = navigator.platform.toLowerCase();
      
      // Windows devices (Windows Hello)
      if (userAgent.includes('windows') || platform.includes('win')) {
        capabilities.windowsHello = true;
        capabilities.fingerprint = true;
        capabilities.laptopBiometric = true;
      }
      
      // macOS devices (Touch ID)
      if (userAgent.includes('mac') || platform.includes('mac')) {
        capabilities.touchId = true;
        capabilities.fingerprint = true;
        capabilities.laptopBiometric = true;
      }
      
      // Linux devices (Fingerprint readers)
      if (userAgent.includes('linux') || platform.includes('linux')) {
        capabilities.linuxFingerprint = true;
        capabilities.fingerprint = true;
        capabilities.laptopBiometric = true;
      }
      
      // iOS devices (Touch ID / Face ID)
      if (userAgent.includes('iphone') || userAgent.includes('ipad')) {
        capabilities.touchId = true;
        capabilities.faceId = true; // Modern iOS devices support both
        capabilities.fingerprint = true;
      }
      
      // Android devices
      if (userAgent.includes('android')) {
        capabilities.fingerprint = true;
        capabilities.androidBiometric = true;
      }
    }
  } catch (error) {
    console.log('Error detecting biometric capabilities:', error);
  }

  return capabilities;
};

export const isLaptopDevice = (): boolean => {
  const userAgent = navigator.userAgent.toLowerCase();
  const platform = navigator.platform.toLowerCase();
  
  // Check for laptop/desktop indicators
  return (
    userAgent.includes('windows') || 
    userAgent.includes('mac') || 
    userAgent.includes('linux') ||
    platform.includes('win') ||
    platform.includes('mac') ||
    platform.includes('linux')
  ) && !isMobileDevice();
};

export const isMobileDevice = (): boolean => {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
};

export const getLaptopBiometricName = (): string => {
  const userAgent = navigator.userAgent.toLowerCase();
  const platform = navigator.platform.toLowerCase();
  
  if (userAgent.includes('windows') || platform.includes('win')) {
    return 'Windows Hello Fingerprint';
  } else if (userAgent.includes('mac') || platform.includes('mac')) {
    return 'MacBook Touch ID';
  } else if (userAgent.includes('linux') || platform.includes('linux')) {
    return 'Linux Fingerprint Reader';
  } else {
    return 'Laptop Biometric Sensor';
  }
};

export const getMobileBiometricName = (): string => {
  const userAgent = navigator.userAgent.toLowerCase();
  
  if (userAgent.includes('iphone') || userAgent.includes('ipad')) {
    return 'Touch ID / Face ID';
  } else if (userAgent.includes('android')) {
    return 'Fingerprint / Biometric';
  } else if (userAgent.includes('windows')) {
    return 'Windows Hello';
  } else {
    return 'Platform Biometric';
  }
};

export const getBiometricDeviceName = (): string => {
  return isLaptopDevice() ? getLaptopBiometricName() : getMobileBiometricName();
};

export const createWebAuthnOptions = (username: string, challenge?: Uint8Array): PublicKeyCredentialCreationOptions => {
  const challengeBuffer = challenge || new Uint8Array(32);
  if (!challenge) {
    crypto.getRandomValues(challengeBuffer);
  }

  return {
    challenge: challengeBuffer,
    rp: {
      name: "Biometric Authentication App",
      id: window.location.hostname,
    },
    user: {
      id: new TextEncoder().encode(username),
      name: username,
      displayName: username,
    },
    pubKeyCredParams: [
      { alg: -7, type: "public-key" }, // ES256
      { alg: -257, type: "public-key" } // RS256
    ],
    authenticatorSelection: {
      authenticatorAttachment: "platform",
      userVerification: "required",
      requireResidentKey: false,
    },
    timeout: 60000,
    attestation: "direct"
  };
};

export const createWebAuthnAssertionOptions = (challenge?: Uint8Array): PublicKeyCredentialRequestOptions => {
  const challengeBuffer = challenge || new Uint8Array(32);
  if (!challenge) {
    crypto.getRandomValues(challengeBuffer);
  }

  return {
    challenge: challengeBuffer,
    timeout: 60000,
    userVerification: "required",
    rpId: window.location.hostname,
  };
}; 