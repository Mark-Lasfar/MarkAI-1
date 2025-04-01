// frontend/src/lib/auth.js (Enhanced)
import { GoogleAuthProvider, signInWithPopup, signOut } from 'firebase/auth'
import { auth } from './firebase'

export const googleProvider = new GoogleAuthProvider()

export const signInWithGoogle = async () => {
  try {
    const result = await signInWithPopup(auth, googleProvider)
    const user = result.user
    
    // Verify/Register user in backend
    const response = await fetch('/api/auth/google', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        uid: user.uid,
        email: user.email,
        name: user.displayName,
        photoURL: user.photoURL
      })
    })
    
    return await response.json()
  } catch (error) {
    throw error
  }
}

export const logout = async () => {
  await signOut(auth)
  await fetch('/api/auth/logout', { method: 'POST' })
}