# ModerAItor

An automatic moderator for public forums. Created for the
`https://databricks-hackathon-2023.devpost.com/` hackaton.

## Introduction

ModerAItor is an AI powered moderator for public forums. Given a post's URL, it
will parse all the comments and flag them according to whether or not they comply
with some user established rules. Unlike existing bots, that use heuristic rules
for moderation, ModerAItor uses Large Language Models (LLMs), which makes it
able to intelligently flag comments given some rules.

## Getting Started

To use `moderaitor`, you must have `docker` and `docker compose` installed in
your system. To deploy the application, you have to set a set of secrets first:

- `docker/HUGGINGFACEHUB_API_TOKEN.secret`: file containing `HUGGINGFACEHUB_API_TOKEN`
- `docker/praw_client_id.secret`: file containing [praw](https://praw.readthedocs.io/en/stable/getting_started/quick_start.html)'s `praw_client_id`
- `docker/praw_client_secret.secret`: file containing [praw](https://praw.readthedocs.io/en/stable/getting_started/quick_start.html)'s `praw_client_secret`

For the hackaton, a public bucket has been created to saved the moderated comments.
If you want to use this repository after the hackaton, you have to create an
AWS S3 Bucket to save the flagged comments.

You also need to set your AWS secret access key and access key id on a `AWS.env`
file inside the `docker` folder that would look like this:

```
AWS_ACCESS_KEY_ID=<key-id>
AWS_SECRET_ACCESS_KEY=<access-id>
```

Finally, execute this command:

```bash
make run-app
```

Or this command if you have created a new S3 bucket:

```bash
COMMENTS_BUCKET="name-of-bucket" make run-app
```

After the app is running (you should see `Uvicorn running on http://0.0.0.0:8000`),
you can send queries to it. For example:

```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "url": "https://www.reddit.com/r/news/comments/148lkof/trump_surrenders_to_federal_custody_in_classified/",
  "rules": "It is not allowed to use offensive words.",
  "max_comments": 10
}' http://localhost:8000/moderate_post/
```

You will can see on the logs the results of the moderation. In addition, all these
labeled comments are saved on the S3 bucket mentioned previously.

Now we know that ModerAItor works. However, you may be interested in having a
human in the loop to check whether the moderation process was good and potentially
make ModerAItor more intelligent. To do this, you can use `label-studio`, a powerful
app to annotate data.

Before using it, you have to install `label_studio_sdk`:

```bash
python -m pip install label-studio
python -m pip install label-studio-sdk
```

Set the following environment variables in the `LABEL_STUDIO.env` file:

- LABEL_STUDIO_USERNAME
- LABEL_STUDIO_PASSWORD
- LABEL_STUDIO_USER_TOKEN

These variables contain the credentials for a new user, which will be used to
set up the project in label studio.

Additionally, you will need an AWS S3 bucket for the human-annotated comments.
For the hackaton, a public bucket is already available.

Finally, execute the following command:

```bash
make run-annotator
```

Or, alternatively, this one if you created your own S3 buckets:

```bash
COMMENTS_BUCKET="name-of-bucket" ANNOTATION_BUCKET="name-of-bucket" make run-app
```

Now, visit `http://0.0.0.0:8080/`, where you can create a new user and start
annotating the AI moderated comments!
