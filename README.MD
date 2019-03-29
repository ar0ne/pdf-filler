# Intro

An Example of AWS Lambdas function for generating PDFs. This project includes [PDFtk](https://www.pdflabs.com/docs/install-pdftk-on-redhat-or-centos/) binary and the ligcj shared library, because AWS Lambda runs on Amazon Linux, which doesn't support PDFtk or GCJ.
For deployment to AWS I'd suggest to use [Zappa](https://github.com/Miserlou/Zappa). For it you just need to create S3 bucket and add it to `zappa_settings.json`. 

## How to use

`$ pip install zappa`

`$ zappa init`

`$ zappa deploy dev`

If there are no issue then you can fill out PDF by REST API.

```
$ curl --request POST \
  --url https://<your-aws-lambda-url>/pdf/test \
  --header 'content-type: application/json' \
  --data '{
  "Given Name Text Box": "Jon",
  "Family Name Text Box": "Doe",
  "House nr Text Box": "21",
  "Address 2 Text Box": "GA 12345-6789, US",
  "Postcode Text Box": "123456",
  "Country Combo Box": "USA",
  "Height Formatted Field": "180",
  "City Text Box": "Atlanta",
  "Driving License Check Box": "On",
  "Favourite Colour List Box": "Green",
  "Language 1 Check Box": "Yes",
  "Language 2 Check Box": "No",
  "Language 3 Check Box": "Yes",
  "Language 4 Check Box": "Off",
  "Language 5 Check Box": "Off",
  "Gender List Box": "Man",
  "Address 1 Text Box": "PO Box 00001, Atlanta"
}'
```

## API

```
GET: /pdf/ - get list of supported PDF files
GET: /pdf/<pdfname>?format={pairs,keys} - get information about fillable PDF
POST: /pdf/<pdfname> - generate filled PDF file
```