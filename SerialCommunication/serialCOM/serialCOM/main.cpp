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
int _tmain(int argc, _TCHAR* argv[])
{
	Serial* SP = new Serial("\\\\.\\COM4");    // adjust as needed
	string input;
	int i = 0;

	if (SP->IsConnected())
		printf("We're connected\n");

	ofstream MyFile("filename.txt");

	char incomingData[256] = "";			// don't forget to pre-allocate memory
	//printf("%s\n",incomingData);
	int dataLength = 255;
	int readResult = 0;

	auto t1 = chrono::steady_clock::now();
	auto t2 = chrono::steady_clock::now();
	auto duration = 0;
	auto counter = 0;
	auto counter2 = 0;

	Sleep(1);

	while (duration <= 1000000)
	{
		readResult = SP->ReadData(incomingData, dataLength);
		// printf("Bytes read: (0 means no data available) %i\n",readResult);
		incomingData[readResult] = 0;
		t2 = chrono::steady_clock::now();
		duration = chrono::duration_cast<chrono::microseconds>(t2 - t1).count();
		MyFile << incomingData;
		++counter2;
		// free(incomingData);
		
	}
	MyFile << duration;
	cout << format("{}, {}\n", counter, counter2);
	MyFile.close();
	return 0;
}
