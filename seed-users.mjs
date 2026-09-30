import { initializeApp } from "firebase/app";
import { getFirestore, collection, addDoc } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyAb1Fbs8Y36BZ8rnIUZBjocc-m0Em_PgcQ",
  authDomain: "datapulseapp-20237.firebaseapp.com",
  projectId: "datapulseapp-20237",
  storageBucket: "datapulseapp-20237.firebasestorage.app",
  messagingSenderId: "459433026519",
  appId: "1:459433026519:web:102f1f951bcb91d306e192",
  measurementId: "G-RFN5ZZTE6W"
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

const usersData = [
  { name: "Muleta T.", email: "muletagegse605@gmail.com", role: "Admin", orgId: "ORG-DEMO" },
  { name: "Abebe K.", email: "abebe@company.com", role: "Manager", orgId: "ORG-DEMO" },
  { name: "Sara L.", email: "sara@company.com", role: "Analyst", orgId: "ORG-DEMO" },
  { name: "Dawit M.", email: "dawit@company.com", role: "Viewer", orgId: "ORG-DEMO" }
];

async function seedUsers() {
  console.log("Users galchuun jalqabame...");
  for (const user of usersData) {
    try {
      await addDoc(collection(db, "users"), user);
      console.log(`Milkaa'eera: ${user.email}`);
    } catch (e) {
      console.error(`Dogoggora: ${user.email}`, e.code);
    }
  }
  console.log("Users hundi milkaa'een galameera!");
}

seedUsers();
