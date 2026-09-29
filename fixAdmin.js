const admin = require('firebase-admin');
const serviceAccount = require('./serviceAccountKey.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

const db = admin.firestore();
const auth = admin.auth();

// Email usericha admin taasisuu barbaaddu as galchi
const targetEmail = 'muletalegese605@gmail.com';

async function fixAdmin() {
  try {
    console.log('User email irraa barbaadaa jira...');
    
    // 1. Authentication irraa UID argadhu
    const user = await auth.getUserByEmail(targetEmail);
    const uid = user.uid;
    console.log(`MILKAA! UID argameera: ${uid}`);

    // 2. Firestore keessatti admins document uumi ykn sirreessi
    await db.collection('admins').doc(uid).set({
      role: 'admin',
      email: targetEmail,
      updatedAt: admin.firestore.FieldValue.serverTimestamp()
    }, { merge: true });

    console.log(`SUCCESS! User ${targetEmail} amma admin ta'eera.`);
    console.log(`Document ID: ${uid}`);
  } catch (error) {
    console.error('DOGOGGORA:', error.message);
  }
}

fixAdmin();
