const { initializeApp } = require('firebase/app');
const { getAuth, signInWithEmailAndPassword } = require('firebase/auth');
const { getFirestore, doc, getDoc } = require('firebase/firestore');

// Config haaraa (kan e234e57dda... fi G-P463... qabu)
const firebaseConfig = {
  apiKey: "AIzaSyAb1Fbs8Y36BZ8rnIUZBjocc-m0Em_PgcQ",
  authDomain: "datapulseapp-20237.firebaseapp.com",
  databaseURL: "https://datapulseapp-20237-default-rtdb.europe-west1.firebasedatabase.app",
  projectId: "datapulseapp-20237",
  storageBucket: "datapulseapp-20237.firebasestorage.app",
  messagingSenderId: "459433026519",
  appId: "1:459433026519:web:e234e57dda2ec80c06e192",
  measurementId: "G-P463V21YRV"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

// --- HUBACHIISA: EMAIL FI PASSWORD KEE GALCHI ---
const ADMIN_EMAIL = "muletalegese605@gmail.com"; 
const ADMIN_PASSWORD = "Mlt@0909"; 
// ------------------------------------------------

async function checkAdmin() {
  try {
    console.log("1. Yeroo amma seenaa jira (Signing in)...");
    const userCredential = await signInWithEmailAndPassword(auth, ADMIN_EMAIL, ADMIN_PASSWORD);
    const uid = userCredential.user.uid;
    console.log(`   ✅ Milkaa'inaan seenee jira. UID kee: ${uid}`);

    console.log(`\n2. Firestore keessaa admins/${uid} dubbisaa jira...`);
    const docRef = doc(db, 'admins', uid);
    const docSnap = await getDoc(docRef);

    if (docSnap.exists()) {
      console.log("   ✅ Document ɗin argameera!");
      const data = docSnap.data();
      console.log("   Role keessan:", data.role);
      
      if (['super', 'admin', 'support'].includes(data.role)) {
        console.log("   ✅ Role ɗin kee sirrii dha. Admin ta'uu qabda!");
      } else {
        console.log("   ❌ Role ɗin kee sirrii miti. 'super', 'admin', ykn 'support' ta'uu qaba.");
      }
    } else {
      console.log("   ❌ Document ɗin hin argamne!");
      console.log("   Kana jechuun, Document ID ɗin kun UID ɗin kee waliin hin simne.");
      console.log("   Deebi'ii Firebase Console irratti sirreessi.");
    }
  } catch (error) {
    console.error("\n❌ Dogoggorri dhufe:", error.message);
    if (error.code === 'auth/invalid-credential') {
      console.log("   👉 Sirreessi: Email ykn Password ɗin kee sirrii miti.");
    } else if (error.code === 'permission-denied') {
      console.log("   👉 Sirreessi: Firestore Rules kee dubbisuu (read) hin hayyamu. Rules kee sirreessi.");
    } else if (error.code === 'auth/api-key-not-valid') {
      console.log("   👉 Sirreessi: API Key ɗin kee sirrii miti. Config haaraa galchi.");
    }
  }
}

checkAdmin();
