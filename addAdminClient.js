const { initializeApp } = require('firebase/app');
const { getAuth, signInWithEmailAndPassword } = require('firebase/auth');
const { getFirestore, doc, setDoc } = require('firebase/firestore');

const firebaseConfig = {
  apiKey: "AIzaSyAb1Fbs8Y36BZ8rnIUZBjocc-m0Em_PgcQ",
  authDomain: "datapulseapp-20237.firebaseapp.com",
  databaseURL: "https://datapulseapp-20237-default-rtdb.europe-west1.firebasedatabase.app",
  projectId: "datapulseapp-20237",
  storageBucket: "datapulseapp-20237.firebasestorage.app",
  messagingSenderId: "459433026519",
  appId: "1:459433026519:web:102f1f951bcb91d306e192",
  measurementId: "G-RFN5ZZTE6W"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

// --- HUBACHIISA: NEW_ADMIN_UID JIJJIIRI ---
const ADMIN_EMAIL = "muletalegese605@gmail.com"; // Email admin kee
const ADMIN_PASSWORD = "Mlt@0909";               // Password admin kee
const NEW_ADMIN_UID = "USER_UID_AS_KAAI";        // <-- AS UID FAYYADAMAA ADMIN GOCHUU BARBAADDU GALCHI!
// ------------------------------------------

async function addAdmin() {
  try {
    await signInWithEmailAndPassword(auth, ADMIN_EMAIL, ADMIN_PASSWORD);
    console.log("Milkaa'inaan admin keessan seenanii jiru.");

    await setDoc(doc(db, 'admins', NEW_ADMIN_UID), {
      role: 'admin',
      createdAt: new Date()
    });
    
    console.log(`Milkaa'inaan ${NEW_ADMIN_UID} gara admins collectiontti galcheera!`);
    process.exit(0);
  } catch (error) {
    console.error('Dogoggora:', error.message);
    process.exit(1);
  }
}

addAdmin();
