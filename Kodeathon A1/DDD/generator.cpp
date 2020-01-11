#include <bits/stdc++.h>
#include <ctime>
using namespace std;
int main(void)
{
    freopen("t1.in","w",stdout);
    srand(time(NULL));
    long t1,t2,x,n,k;
    int t=50;
    cout<<t<<endl;
    while(t--)
    {
        x=1+rand()%50;
        t1=1+rand()%50;
        t2=1+rand()%50;
        long y=t1+t2;
        k=1+(rand()%y);
        n=rand()%1000000000;
        
        cout<<x<<" "<<t1<<" "<<t2<<" "<<k<<" "<<n<<endl;
    }

}
