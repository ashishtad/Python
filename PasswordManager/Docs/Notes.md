
    STORING NEW PASSWORD WHILE SIGNUP

    - Create a salt and combine it with plain text password and then hash it with SHA 256 algorithm
    - More abot hashing and random salt.
    In the context of password security, a "salt" is a random value that is combined with a password before applying a hash function. The primary purpose of a salt is to prevent attackers from using precomputed tables, called rainbow tables, for efficiently cracking hashed passwords.

Here's why salt is important and how it works:

Preventing Rainbow Table Attacks:

Without a salt, if two users have the same password, they will generate the same hash. An attacker can use precomputed tables (rainbow tables) that map hash values to their corresponding plaintext passwords. This allows them to quickly look up a hash and find the corresponding password.
Salting adds a unique value to each password before hashing, ensuring that even users with the same password will have different hash values.
Unique Hashes for Same Passwords:

When a salt is added to a password before hashing, even if two users have the same password, their hash values will be different due to the unique salt.
This means that attackers must compute rainbow tables for each individual salt value, significantly increasing the computational effort required to crack passwords.
Enhancing Security:

Salting is a critical component of password security because it adds complexity to the hashing process. It mitigates the risk of dictionary attacks and other forms of password cracking.
The use of unique salts per user also prevents attackers from identifying identical passwords across different users in a system.
Randomness and Unpredictability:

A good salt should be random and unpredictable. This randomness ensures that attackers cannot exploit patterns in the salt values.
The use of a strong, unpredictable salt adds an extra layer of defense against various cryptographic attacks.
In the context of password hashing, the salt is typically stored along with the hashed password in a secure database. During authentication, the stored salt is retrieved and combined with the entered password for hashing. This process ensures that even if an attacker gains access to the hashed passwords, they face significant challenges in cracking them due to the unique salts.

- To store the user credentials sqlite DB which is a lightweight relational database is used.

To Do:
Implement the logger module