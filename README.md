# Data Ingestion of Trip Record Data from TLC to AWS S3 using Dagster

This repository contains a data ingestion pipeline that fetches Trip Record Data from the Taxi and Limousine Commission (TLC) in New York, processes it using Dagster, and stores it in AWS S3. The pipeline is designed to automate the data ingestion process, making it easy to collect and store the data for further analysis and use.

![Workflow](https://github.com/noelAngelo/tlc-dagster-s3/blob/main/assets/tlc-dagster-s3.png?raw=true)

## Prerequisites

Before running the data ingestion pipeline, ensure you have the following components set up:

1. **Dagster**: Dagster is a data orchestrator that helps define and run data workflows. Make sure you have installed Dagster and its dependencies.

2. **AWS Account**: You will need an AWS account to store the data in S3. Ensure you have your AWS credentials and access keys ready.

## Getting Started

Follow the steps below to set up the data ingestion pipeline:

1. Clone the repository:

```
git clone https://github.com/your_username/your_repository.git
cd your_repository
```

2. Install the required dependencies:

```
pip install dagster
```

3. Update the `.env` file with your AWS credentials:

In order to use the AWS SDK to interact with S3, you need to provide your AWS access key and secret key. Create a `.env` file in the root of the repository and add the following content:

```dotenv
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
```

**Note:** Never commit the `.env` file to version control. Ensure it is listed in your `.gitignore` file to prevent accidental exposure of sensitive credentials.

## Running the Data Ingestion Pipeline

The data ingestion pipeline is defined in the `pipeline.py` file. To run the pipeline and start ingesting data, execute the following command:

```
dagster pipeline execute -f pipeline.py
```

Dagster will execute the steps defined in the pipeline, which include fetching the Trip Record Data from the TLC API, processing the data, and storing it in AWS S3.

## Contributing

If you would like to contribute to this project, feel free to submit a pull request. We welcome any improvements or bug fixes to the data ingestion pipeline.

## License

This project is licensed under the [MIT License](LICENSE), which allows you to use, modify, and distribute the code for both commercial and non-commercial purposes.

## Contact

For any questions or concerns regarding the data ingestion pipeline or this repository, please feel free to contact us at contact@example.com.

---
**Note**: Make sure to replace `your_username`, `your_repository`, and `contact@example.com` with appropriate values specific to your project.

With this README, users will be able to set up and run the data ingestion pipeline to fetch and store Trip Record Data from the TLC in New York using Dagster and AWS S3. The section in the wiki emphasizes the importance of updating the `.env` file with AWS credentials to enable secure data transfer to S3. Remember to always keep sensitive information, such as AWS credentials, confidential and avoid committing them to version control.
