/*
 * Copyright 2010-2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */

/**
 * @file subscribe_publish_sample.c
 * @brief simple MQTT publish and subscribe on the same topic
 *
 * This example takes the parameters from the aws_iot_config.h file and establishes a connection to the AWS IoT MQTT Platform.
 * It subscribes and publishes to the same topic - "sdkTest/sub"
 *
 * If all the certs are correct, you should see the messages received by the application in a loop.
 *
 * The application takes in the certificate path, host name , port and the number of times the publish should happen.
 *
 */
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <unistd.h>

#include <signal.h>
#include <memory.h>
#include <sys/time.h>
#include <limits.h>

#include "aws_iot_log.h"
#include "aws_iot_version.h"
#include "aws_iot_mqtt_interface.h"
#include "aws_iot_config.h"

int MQTTcallbackHandler(MQTTCallbackParams params) {

	INFO("Subscribe callback");
	INFO("%.*s\t%.*s",
			(int)params.TopicNameLen, params.pTopicName,
			(int)params.MessageParams.PayloadLen, (char*)params.MessageParams.pPayload);

	return 0;
}

void disconnectCallbackHandler(void) {
	WARN("MQTT Disconnect");
	IoT_Error_t rc = NONE_ERROR;
	if(aws_iot_is_autoreconnect_enabled()){
		INFO("Auto Reconnect is enabled, Reconnecting attempt will start now");
	}else{
		WARN("Auto Reconnect not enabled. Starting manual reconnect...");
		rc = aws_iot_mqtt_attempt_reconnect();
		if(RECONNECT_SUCCESSFUL == rc){
			WARN("Manual Reconnect Successful");
		}else{
			WARN("Manual Reconnect Failed - %d", rc);
		}
	}
}

/**
 * @brief Default cert location; NOT USED
 */
char certDirectory[PATH_MAX + 1] = "../../../Python_TrustM_GUI/working_space";

/**
 * @brief Default MQTT HOST URL is pulled from the aws_iot_config.h
 */
char HostAddress[255] = AWS_IOT_MQTT_HOST;

/**
 * @brief Default MQTT port is pulled from the aws_iot_config.h
 */
uint32_t port = AWS_IOT_MQTT_PORT;

/**
 * @brief This parameter will avoid infinite loop of publish and exit the program after certain number of publishes
 */
uint32_t publishCount = 1;

int main(int argc, char** argv) {
	IoT_Error_t rc = NONE_ERROR;
	bool infinitePublishFlag = false;
	int c;

	char rootCA[PATH_MAX + 1];
	char clientCRT[PATH_MAX + 1];
	char clientKey[PATH_MAX + 1];
	char CurrentWD[PATH_MAX + 1];
	char cafileName[] = AWS_IOT_ROOT_CA_FILENAME;
	char clientCRTName[] = AWS_IOT_CERTIFICATE_FILENAME;
	char clientKeyName[] = AWS_IOT_PRIVATE_KEY_FILENAME;
	char mqtt_message[100];
	//~ char host_endpoint[60];
	
	//~ char valueBPM[20];
	char pubtopic[40];
	
	while ((c = getopt (argc, argv, "e:m:t:")) != -1) {
		switch (c) {
			//~ case 'o':
				//~ strncpy(valueSPO2, optarg, sizeof(valueSPO2) );
				//~ DEBUG("valueSPO2 is %s", valueSPO2);
				//~ break;
			//~ case 'b':
				//~ strncpy(valueBPM, optarg, sizeof(valueBPM) );
				//~ DEBUG("valueBPM is %s", valueBPM);
				//~ break;
			case 'e':
				strncpy(HostAddress, optarg, sizeof(HostAddress) );
				DEBUG("Endpoint is %s", HostAddress);
				break;

			case 'm':
				strncpy(mqtt_message, optarg, sizeof(mqtt_message) );
				DEBUG("Publish message is %s", mqtt_message);
				break;

			case 't':
				strncpy(pubtopic, optarg, sizeof(pubtopic) );
				DEBUG("Publish Topic is %s", pubtopic);
				break;

			case '?':
				if (optopt == 'c') {
					ERROR("Option -%c requires an argument.", optopt);
				} else if (isprint(optopt)) {
					WARN("Unknown option `-%c'.", optopt);
				} else {
					WARN("Unknown option character `\\x%x'.", optopt);
				}
				break;
			default:
				ERROR("Error in command line argument parsing");
		}
	}

	INFO("\nAWS IoT SDK Version %d.%d.%d-%s\n", VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH, VERSION_TAG);

	getcwd(CurrentWD, sizeof(CurrentWD));
	sprintf(rootCA, "%s/%s", CurrentWD, cafileName);
	sprintf(clientCRT, "%s/%s", CurrentWD, clientCRTName);
	sprintf(clientKey, "%s/%s", CurrentWD, clientKeyName);

	DEBUG("rootCA %s", rootCA);
	DEBUG("clientCRT %s", clientCRT);
	DEBUG("clientKey %s", clientKey);

	MQTTConnectParams connectParams = MQTTConnectParamsDefault;

	connectParams.KeepAliveInterval_sec = 5; //50; //10
	connectParams.isCleansession = true;
	connectParams.MQTTVersion = MQTT_3_1_1;
	connectParams.pClientID = "CSDK-test-device";
	connectParams.pHostURL = HostAddress;
	connectParams.port = port;
	connectParams.isWillMsgPresent = false;
	connectParams.pRootCALocation = rootCA;
	connectParams.pDeviceCertLocation = clientCRT;
	connectParams.pDevicePrivateKeyLocation = clientKey;
	connectParams.mqttCommandTimeout_ms = 10000; //2000
	connectParams.tlsHandshakeTimeout_ms = 10000; //5000;
	connectParams.isSSLHostnameVerify = true; // ensure this is set to true for production
	connectParams.disconnectHandler = disconnectCallbackHandler;

	INFO("Connecting...");
	rc = aws_iot_mqtt_connect(&connectParams);
	if (NONE_ERROR != rc) {
		ERROR("Error(%d) in aws_iot_mqtt_connect: %s:%d", rc, connectParams.pHostURL, connectParams.port);
	}
	/*
	 * Enable Auto Reconnect functionality. Minimum and Maximum time of Exponential backoff are set in aws_iot_config.h
	 *  #AWS_IOT_MQTT_MIN_RECONNECT_WAIT_INTERVAL
	 *  #AWS_IOT_MQTT_MAX_RECONNECT_WAIT_INTERVAL
	 */
	rc = aws_iot_mqtt_autoreconnect_set_status(true);
	if (NONE_ERROR != rc) {
		ERROR("Unable to set Auto Reconnect to true - %d", rc);
		return rc;
	}

//**********
/*
	MQTTSubscribeParams subParams = MQTTSubscribeParamsDefault;
	subParams.mHandler = MQTTcallbackHandler;
	//subParams.pTopic = "sdkTest/sub";
	subParams.pTopic ="pulsioximeter";
	subParams.qos = QOS_0;

	if (NONE_ERROR == rc) {
		INFO("Subscribing...");
		rc = aws_iot_mqtt_subscribe(&subParams);
		if (NONE_ERROR != rc) {
			ERROR("Error subscribing");
		}
	}
*/

	MQTTMessageParams Msg = MQTTMessageParamsDefault;
	Msg.qos = QOS_0;
	char cPayload[110];
	sprintf(cPayload, "%s", mqtt_message);
	Msg.pPayload = (void *) cPayload;

	MQTTPublishParams Params = MQTTPublishParamsDefault;
	//Params.pTopic = "pulsioximeter";
	Params.pTopic = (void *) pubtopic;
	if (publishCount != 0) {
		infinitePublishFlag = false;
	}
	
	while ((NETWORK_ATTEMPTING_RECONNECT == rc || RECONNECT_SUCCESSFUL == rc || NONE_ERROR == rc)
			&& (publishCount > 0 || infinitePublishFlag)) {

		//Max time the yield function will wait for read messag	es
		rc = aws_iot_mqtt_yield(100);
		if(NETWORK_ATTEMPTING_RECONNECT == rc){
			//INFO("-->sleep");
			sleep(1);
			// If the client is attempting to reconnect we will skip the rest of the loop.
			continue;
		}
		//INFO("-->sleep");
		sleep(1);
		
		INFO("--> Publishing ....");
		INFO("%s", mqtt_message);
		
		Msg.PayloadLen = strlen(cPayload) + 1;
		Params.MessageParams = Msg;
		rc = aws_iot_mqtt_publish(&Params);
/* 			if (rc == MQTT_REQUEST_TIMEOUT_ERROR) {
			WARN("Publish ack not received.\n");
			rc = NONE_ERROR;
		} */

		if (publishCount > 0) {
			publishCount--;
		}

		if(publishCount == 0 && !infinitePublishFlag) {
			break;
		}

	}

	if (NONE_ERROR != rc) {
		ERROR("An error occurred.\n");
	} else {
		INFO("Publish done, device disconnecting...\n");
	}

	return rc;
}
