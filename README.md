<h1> Crypter: An educational end-to-end encryption application </h1>
<img src="crypter.png"
     alt="Not sure what the map has to do with it tbh...but it looks cool"
     style="float: left; margin-right: 10px;" />

<br>
<h2> Introduction </h2>
<p> End-to-end encryption has become a staple on communications online, and it has become a hot-button political issue in several nations, a battle between governments fighting for law enforcement and tech companies fighting for cybersecurity. Given that this political issue requires familiarity with cyber-encryption schemes, and therefore requires familiarity with algorithms and number theory, it can feel daunting to the average, non-technical person.</p> 
<p> So, we've decided to develop a hands-on way of learning about how modern encryption works. We've created a basic messaging app that most people might use, but we've stripped back the curtain and visualized the components of how a message is encrypted and decrypted. In this way, any user can get an idea of what happens to their message when using end-to-end encryption, why it can be complicated, how it's designed to be hard to break, and therefore better understand the discussion surrounding the issue.</p>

<h2> <u> v.1.0 </u> </h2>
<p> The server has been deployed to Google Cloud and should remain active until April 30th, 2021.</p> 
<br>
<p>To run the application, first install the necessary dependencies. Then, navigate to main.py as shown in the file tree below and run with python versions 3 and above. You must create a new account, and upon revisiting the app, login to the account you previously created or create a new account. Logging into an existing account different from your last login is not currently supported. </p> 

<h2> <u> v.0.0 </u> </h2>
<p>Currently, your IP address must be white-listed by the server admin to access the MongoDB.</p> 
<br>
<p>To run the package, first install the necessary dependencies. Then, follow the instructions in the server README to start the server locally. Finally, navigate to main.py and run. </p> 

<pre>
<code>
└── src 
    ├── server
    │   ├── README.md
    └── client
        ├── main.py
        ├── query.py
        └── encrypt
            └── rsa.py
</code>
</pre>