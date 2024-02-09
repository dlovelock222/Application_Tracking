// Chakra imports
import {
  Flex,
  Table,
  Tbody,
  Text,
  Th,
  Thead,
  Tr,
  useColorModeValue
} from "@chakra-ui/react";
// Custom components
import Card from "components/Card/Card.js";
import CardBody from "components/Card/CardBody.js";
import CardHeader from "components/Card/CardHeader.js";
import TablesProjectRow from "components/Tables/TablesProjectRow";
import TablesTableRow from "components/Tables/TablesTableRow";
import React, { useEffect, useState } from 'react';
import { tablesProjectData, tablesTableData } from "variables/general";
import userAuthInstance from 'variables/UserAuthentication.js'
import Email from 'variables/Email';
import axios from 'axios'

function Tables() {
  const textColor = useColorModeValue("gray.700", "white");
  const borderColor = useColorModeValue("gray.200", "gray.600");
  const [currEmails, setCurrEmails] = useState([]);
  const emailSearchParams = [];
  useEffect(() => {
    const fetchEmails = async () => {
      if(userAuthInstance.isUserLoggedIn()){
        const userID = userAuthInstance.getUserDetails().id;
        try {
          const response = await axios.get('https://gmail.googleapis.com/gmail/v1/users/me/messages', {
            headers: {
              Authorization: `Bearer ${userID}`,
            },
            params: {
              maxResults: 50,
            },
          });
          const emails = Array.from(response.data.messages).map(async (message) => {
            const emailResponse = await fetch(`https://gmail.googleapis.com/gmail/v1/users/me/messages/${message.id}`, {
              method: 'GET',
              headers: new Headers({ Authorization: `Bearer ${userID}` }),
            });
            const info = await emailResponse.json();
  
            const headers = info.payload.headers;
            const sender = headers.find((header) => header.name === 'From').value;
            const subject = headers.find((header) => header.name === 'Subject').value;
            const snippet = info.snippet;

            const apiUrl = new URL('http://127.0.0.1:5000/predict_job_application');
            const params = new URLSearchParams({
                sender: sender,
                subject: subject,
                snippet: snippet,
            });
            apiUrl.search = params;
            try {
              const chanceOfApplication = await fetch(apiUrl, {
                method: 'GET',
              });
              if (chanceOfApplication.ok) {
                const result = await chanceOfApplication.json();
                console.log('Prediction:', result.prediction);
              } else {
                  console.error('Error fetching data:', chanceOfApplication.statusText);
              }
            }
            
  
            return new Email(subject, sender, snippet, "", chanceOfApplication['prediction']);
          });
          const resolvedEmails = await Promise.all(emails);
          const jsonEmails = JSON.stringify(emails, null, 2);
          // fs.writeFileSync('model/email_data/emails.json', jsonEmails);
          setCurrEmails(resolvedEmails);
          //sort the emails by probability that they are related to a job application
        } catch (error) {
          console.error('Error fetching user email data:', error.message);
        }
      }
   };
  // Check if the access token is available before making the request
  if (userAuthInstance.isUserLoggedIn()) {
    fetchEmails();
  }
  }, [emailSearchParams, currEmails, userAuthInstance]);
  return (
    <Flex direction="column" pt={{ base: "120px", md: "75px" }}>
      <Card overflowX={{ sm: "scroll", xl: "hidden" }} pb="0px">
        <CardHeader p="6px 0px 22px 0px">
          <Text fontSize="xl" color={textColor} fontWeight="bold">
            Inbox
          </Text>
        </CardHeader>
        <CardBody>
          <Table variant="simple" color={textColor}>
            <Thead>
              <Tr my=".8rem" pl="0px" color="gray.400" >
                <Th pl="0px" borderColor={borderColor} color="gray.400" >
                  Subject
                </Th>
                <Th borderColor={borderColor} color="gray.400" >Sender</Th>
                <Th borderColor={borderColor} color="gray.400" >Snippet</Th>
                <Th borderColor={borderColor}></Th>
              </Tr>
            </Thead>
            <Tbody>
              {
                currEmails.map((row, index, arr) => {
                  return (
                    <TablesTableRow
                      key={index}
                      subject={row.getSubject()}
                      sender={row.getSender()}
                      snippet={row.getSnippet()}
                      date={row.getDate()}
                      isLast={index === arr.length - 1}
                    />
                  );
                })
              }
            </Tbody>
          </Table>
        </CardBody>
      </Card>
    </Flex>
  );
}

export default Tables;
