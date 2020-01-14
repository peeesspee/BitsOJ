#include <bits/stdc++.h>
using namespace std;
int main ()
{
    signed long long int t, n,temp;
    cin>>t;
    while(t--)
    {
        signed long long int num;
        cin >> num;
        if (num%2 == 0)
            cout << num/2 <<endl;
        else if (num%2 == 1)
        {
            temp = (num-1)/2 - num;
            cout << temp << endl;
        }
     }
 return 0;
}
