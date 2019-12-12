#include<bits/stdc++.h>
#include<time.h>
#include<cstdlib>
using namespace std;
int main(void)
{   srand(time(NULL));
    freopen("t1.in","w",stdout);
    //freopen("test01.in","r",stdin);
    long tests, n, arr[10000], i,j,x,y;
    tests=100;
    cout<<tests<<endl;

    for(j=0;j<50;j++)
    {
        n=(rand()%100)+1;
        cout<<n<<"\n";
        for(i=0;i<n;i++)
        {   x=(rand()%100);
            cout<<x<<" ";
        }
        cout<<"\n";
        fflush(stdout);
    }
    for(j=50;j<98;j++)
    {
        n=(rand()%1000)+1;
        cout<<n<<"\n";
        for(i=0;i<n;i++)
        {   x=(rand()%100000);
            cout<<x<<" ";
        }
        cout<<endl;
    }
    for(j=98;j<100;j++)
    {
        n=(rand()%1000000)+1;
        cout<<n<<"\n";
        for(i=0;i<n;i++)
        {   x=(rand()%10000000);
            cout<<x<<" ";
        }
        cout<<endl;
    }
}
