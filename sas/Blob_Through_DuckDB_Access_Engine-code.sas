/* Change this to your blob name (with the full path including containers and subfolders*/
%let blob_name="az://output-data/Test_Lou/ALL_GOLF.parquet" ;

/* Create libref for DuckDB */

libname newduck sasioduk ;

/* Offline:  Ensure you have set up a new credential in your Viya environment, with the following characteristics:

- Linked to your SAS user identity
- Holds the storage account as the user id (optional)
- Holds the connection string to the Azure storage account as the password

*/;

/* Retrieve Blob credentials and details from credentials service */

filename resp temp;
proc http
  method=GET
  out=resp
  url="https://viya.ext-post-aks.unx.sas.com/credentials/domains/AzureBlobConStringAuth/secrets"
  oauth_bearer = sas_services;
 headers
  "Accept"="application/vnd.sas.credential+json";
run;
 
/* Retrieve credentials and store in macro variables.  The azureAccount variable is not used, but populated for convenience.  */
libname output json fileref=resp;
data _null_;
 set output.alldata;
 where p2 in ("userId","password");
 by P V;
 if P2 = "userId" then call symput('azureAccount',Value);
 if P2 = "password" then call symput("connectionStringb64", Value);

run;

/* Credential service base64 encodes by default;  decode the same */;

%let connectionString="%sysfunc(inputc(&connectionStringb64.,$base64x32767.))";


/* Execute query to read (write is currently not supported) data from Azure Blob Storage using DuckDB */

PROC SQL;
    /* connect using the SASIODUK configuration profile */
	connect using newduck;

    execute(
/*  Prepare DuckDB inside SAS to support cloud-based data access. */                                     
			SET extension_directory = '/tmp/.extensions';
			SET azure_transport_option_type = 'curl';
            INSTALL httpfs;
			LOAD httpfs;
			INSTALL azure;
			LOAD azure;

            /* Authenticate to Azure using Config */
			CREATE OR REPLACE SECRET secret_config (
    			TYPE         azure,
                CONNECTION_STRING  &connectionString.
            );
            
      ) by newduck;

      select * from connection to newduck(
      
            select count(*) as nbr_records from &blob_name.
 
            );
    
      create table newduck.NEWDATA as 
            select * from connection to newduck(

            select * from &blob_name. LIMIT 10
            
            );


        /* note that currently, the SAS/Access Interface to DuckDB does not support writing to Azure Blob Storage directly from SAS. 
           The following code is commented out, but can be used in a DuckDB session to write data to Azure Blob Storage.
           You can use the DuckDB CLI or other interfaces to execute this code directly.
        */    
        /* execute(
            copy(
             select * from 'az://output-data/Test_Lou/ALL_GOLF.parquet' 
            ) TO &another_blob_name. (FORMAT 'parquet') 
              



        ) by newduck;
        */

quit;

proc datasets lib=newduck;
quit;