# Lambda KMS Encryptor

This Cloudformation script creates a Lambda function that uses KMS to encrypt plaintext using the supplied KMS key

The Lambda expects to receive an event of the form:

```
{
	"KmsArn" : <A valid KMS key arn, created in the current AWS Region>,
	"PlainText" : <Data to be encrypted, up to 4096 bytes long>
}
```

Exceptions will be thrown if the KMS key is not created in the current AWS Region and Account.

The Lambda returns the encrypted data if successful, as a base64 encoded string.

The script creates the following:

![alt text](https://github.com/gford1000-aws/lambda-kms-encryptor/blob/master/Encryptor.png "Script per designer")


## Arguments

| Argument                      | Description                                                                     |
| ----------------------------- |:-------------------------------------------------------------------------------:|
| XRayTraceMode                 | If XRay tracing is enabled, then this parameter specifies the type of tracing   |


## Outputs

| Output               | Description                                            |
| ---------------------|:------------------------------------------------------:|
| Lambda               | The Arn of the Lambda function                         |


## Licence

This project is released under the MIT license. See [LICENSE](LICENSE) for details.
