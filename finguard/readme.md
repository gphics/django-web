# I finally crossed the finish line. 🏁 FinGuard is officially done!

Building this application tested every bit of my patience, especially when university exams hit right in the middle of development. Trying to study while my brain just wanted to solve coding bugs was incredibly frustrating, but I had to maximize every single minute in the IDE.



I wanted to share the real engineering battles, pivots, and breakthroughs from this build:

🔒 Privacy First (No Bank Syncing)

I deliberately chose not to connect this to banking APIs. Users manually input transactions so they know exactly what they are sharing. To keep it from being tedious, I built a bulk upload feature so you can just drop a formatted CSV file and instantly pull in hundreds of rows.



📊 Clean Data with Pandas

To avoid writing messy, repetitive scripts for financial statistics, I built performant Pandas utility classes. This abstracted away all the boring boilerplate code, giving me clean, accurate data insights without the headache.



🧠 The ML Model & Hosting Realities

I originally set up Celery for background tasks, but finding free cloud hosting for background workers is almost impossible. So, I shifted the logic back to the main request flow while keeping it lightning-fast.

Also, saving model instances per user was a memory nightmare. Plus, retraining a model on tiny amounts of data is redundant. My solution? Once a user hits 5 transactions, it simply unlocks a button on the frontend. Click it, the backend builds the IsolationForest model on the fly, runs the prediction, flashes the anomalies, and completely discards the model. No saved data, zero idle memory footprint.



💻 Unlearning Old Frontend Habits

I’ve always used SCSS, so moving to Tailwind CSS felt completely alien at first. It was frustrating unlearning custom stylesheets, but the development speed eventually won me over. I also purposely ditched Redux. Instead of over-engineering, I kept the Next.js frontend simple and state-light.



🛠️ Dev Automation & Backend Wins

Tired of typing long, annoying terminal commands every time I wanted to test locally, I wrote a quick shell script. Now, one command boots the Django backend, Postgres, and Next.js frontend together. On the API side, django-filterset became my best friend for querying complex localized data without lagging.



The Tech Stack: Next.js, Tailwind, Django, DRF, django-filter, Pandas, PostgreSQL, AWS S3, and Scikit-learn.



### Visit the website through this link: https://finguard-xi.vercel.app/



Software engineering isn't just about writing code—it's about surviving cloud hosting constraints, memory issues, and life schedules.



#Python #Django #NextJS #TailwindCSS #MachineLearning #SoftwareEngineering #DataScience #AWS #FinGuard #DevOps #Pandas





