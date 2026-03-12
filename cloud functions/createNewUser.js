const functions = require("firebase-functions");
const admin = require("firebase-admin");
// To avoid deployment errors, do not call admin.initializeApp() in your code

if (!admin.apps.length) {
  admin.initializeApp();
}

exports.createNewUser = functions.https.onCall(async (data, context) => {
  // Перевірка, чи викликає функцію авторизований юзер (можна додати перевірку на адміна)
  if (!context.auth) {
    throw new functions.https.HttpsError(
      "unauthenticated",
      "The function must be called while authenticated.",
    );
  }

  const email = data.email;
  const password = data.password;
  const displayName = data.displayName;
  const role = data.role;
  const workspaceRef = data.workspaceRef;

  try {
    // 1. Створюємо користувача в Auth
    const userRecord = await admin.auth().createUser({
      email: email,
      password: password,
      displayName: displayName,
    });

    // 2. Створюємо запис у колекції 'users' (Firestore)
    await admin
      .firestore()
      .collection("users")
      .doc(userRecord.uid)
      .set({
        email: email,
        display_name: displayName,
        workspace_ref: admin.firestore().doc(workspaceRef),
        workspace_role: role,
        created_time: admin.firestore.FieldValue.serverTimestamp(),
        uid: userRecord.uid,
      });

    return { success: true, message: `User ${email} created successfully.` };
  } catch (error) {
    console.error("Error creating user:", error);
    throw new functions.https.HttpsError("unknown", error.message, error);
  }
});
