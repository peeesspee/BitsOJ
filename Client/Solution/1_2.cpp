#include<bits/stdc++.h>
#include<cstdio>
using namespace std;
typedef long long int lli;
int main()
{   lli t;
   // freopen("input.in","r",stdin);
   // freopen("output.ans","w",stdout);
    cin>>t;
    while(t--)
    {   lli x1,x2,x3,x4,y1,y2,y3,y4;
        cin>>x1>>y1;
        cin>>x2>>y2;
        cin>>x3>>y3;
        cin>>x4>>y4;
        double x=(x1+x3)/2.0;
        double y=(y1+y3)/2.0;
        cout<<x<<" "<<y<<"\n";
    }
    return 0;
}
