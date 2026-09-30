import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-app.js";
import { getFirestore, collection, getDocs } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js";

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

document.addEventListener('DOMContentLoaded', async () => {
  try {
    const querySnapshot = await getDocs(collection(db, "sales"));
    let totalRows = 0;
    let totalRevenue = 0;

    querySnapshot.forEach((doc) => {
      const data = doc.data();
      totalRevenue += data.revenue || 0;
      totalRows++;
    });

    // UI irratti agarsiisuuf (ID'oonni HTML kee waliin tokko ta'uu qabu)
    const totalRowsEl = document.getElementById('total-rows');
    if (totalRowsEl) totalRowsEl.innerText = totalRows;

    const grossSalesEl = document.getElementById('gross-sales');
    if (grossSalesEl) grossSalesEl.innerText = `ETB ${totalRevenue.toLocaleString()}`;

    console.log("Total Rows from Firestore:", totalRows);
    console.log("Total Revenue from Firestore:", totalRevenue);
  } catch (error) {
    console.error("Dogoggora Firestore:", error);
  }
});
