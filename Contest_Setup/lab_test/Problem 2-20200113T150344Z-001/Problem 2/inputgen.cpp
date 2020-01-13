#include <bits/stdc++.h>
using namespace std;
int main()
{
    srand(time(NULL));
    freopen("inputfile.in","w",stdout);
    int t=100000,n;
    cout<<t<<"\n";
    while(t--)
    {
      long long int n=rand()%1000000000+1;
      cout<<n<<endl;
    }
    return 0;
}
