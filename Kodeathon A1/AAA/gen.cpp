#include<bits/stdc++.h>
#include<time.h>
#include<cstdio>
using namespace std;
typedef long long int lli;
int main()
{   srand(time(NULL));
    freopen("input.in","w",stdout);
    lli T=1000;
    cout<<T<<"\n";
    while(T--)
    {   lli X1,X2;
        X1=(rand()%1000000);
        X2=(rand()%1000000);
        if(X2<X1)
        {   swap(X2,X1);
        }
        cout<<X1<<" "<<0<<endl;
        cout<<X2<<" "<<0<<endl;
        lli X=(X1+X2)/2;
        lli Y=(rand()%1000000);
        cout<<X<<" "<<Y<<endl;
        lli X3=X-X1;
        X3=X1-X3;
        cout<<X3<<" "<<Y<<endl;
        //cout<<endl;
    }
}
