#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

int main()
{
	while (true){
		int n;
		cin >> n;
		if (n == 0){ break; }

		vector<int> data(n);
		vector<int> output;
		for (int i = 0; i < n; i++){
			cin >> data[i];
		}

		for (int i = n; i > 0; i--){
			output.insert(output.begin() + data[i - 1], i);
		}

		//printing
		for (int i = 0; i < n - 1; i++){
			cout << output[i] << ",";
		}
		cout << output[n - 1] << endl;
	}
	return 0;
}
