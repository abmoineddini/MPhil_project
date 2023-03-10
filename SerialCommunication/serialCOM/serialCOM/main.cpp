#include <stdio.h>
#include <tchar.h>
#include "SerialClass.h"	// Library described above
#include <string>
#include <format>
#include <iostream>
#include <chrono>
#include <fstream>

using namespace std;
using std::cout;
using std::format;
using std::string;

// application reads from the specified serial port and reports the collected data
int main(int argc, char* argv[])
{	
	// Setting serical COM channels
	cout << "Starting\n";
	string COMnum = "\\\\.\\";
	COMnum += argv[1];
	cout << format("Comport is: {}\n", COMnum);
	const char* COMPort = COMnum.c_str();
	Serial* SP = new Serial(COMPort);    // adjust as needed

	// Setting Number of Channels
	const char* ChannelNumber = argv[2];
	int sendDataLength = 1;

	// Setting test period
	unsigned long int t = ((unsigned int)*argv[3]-48)*1000000;
	cout << format("Data collection period is: {}us\n", t);

	string input;
	int i = 0;

	if (SP->IsConnected())
		printf("We're connected\n");

	ofstream MyFile("temp.txt");

	char incomingData[256] = "";			// don't forget to pre-allocate memory
	//printf("%s\n",incomingData);
	int dataLength = 255;
	int readResult = 0;

	auto t1 = chrono::steady_clock::now();
	auto t2 = chrono::steady_clock::now();
	auto duration = 0;
	auto counter = 0;
	auto counter2 = 0;

	SP->WriteData(ChannelNumber, sendDataLength);

	Sleep(1);

	while (duration <= t)
	{
		readResult = SP->ReadData(incomingData, dataLength);
		incomingData[readResult] = 0;
		t2 = chrono::steady_clock::now();
		duration = chrono::duration_cast<chrono::microseconds>(t2 - t1).count();
		MyFile << incomingData;
		++counter2;
	}
	MyFile << duration;
	cout << format("{}, {}\n", counter, counter2);
	MyFile.close();
	cout << format("Done!\n");
	return 0;
}
