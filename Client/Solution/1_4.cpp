//Sachinam Srivastava
#include <bits/stdc++.h>
using namespace std;
#define ll long long




class KMP_String_Matching 
{ 
    public:
    
    ll KMPSearch(string pat, string txt) 
    { 
        ll M = pat.length(); 
        ll N = txt.length(); 
        
        
        
        ll lps[M]; 
        ll j = 0; 
   
         
        computeLPSArray(pat,M,lps); 
   
        ll i = 0;   
        ll res = 0;  
        ll next_i = 0;   
          
        while (i < N) 
        { 
            if (pat[j] == txt[i] || txt[i]=='#') 
            { 
                
                j++; 
                i++; 
            } 
            if (j == M) 
            { 
                j = lps[j-1]; 
                res++; 
                if (lps[j]!=0) 
                {
                    i = ++next_i;
                }
                j = 0; 
            } 
            else if (i < N && pat[j] != txt[i] && txt[i]!='#') 
            { 
                
                if (j != 0) 
                {
                    j = lps[j-1]; 
                    ++next_i;
                }
                else
                {
                    i = i+1;
                    ++next_i;
                }
            } 
        } 
        return res; 
    } 
   
    void computeLPSArray(string pat, ll M, ll lps[]) 
    { 
        
        ll len = 0; 
        ll i = 1; 
        lps[0] = 0;  
   
        while (i < M) 
        { 
            if (pat[i] == pat[len]) 
            { 
                len++; 
                lps[i] = len; 
                i++; 
            } 
            else  
            { 
                
                if (len != 0) 
                { 
                    len = lps[len-1]; 
   
                } 
                else 
                { 
                    lps[i] = len; 
                    i++; 
                } 
            } 
        } 
    } 
   
} 
;




int main() 
{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    cout.tie(NULL);
    string a,b,s,add_string="#",add_string2;
    ll t,n,i,j,k,l,m,x,y,flag=0;
    cin>>a;
    cin>>b;
    for(i=0;i<a.length();i++)
    {
        if(a[i]>='a' && a[i]<='z')
        {
            s.append(a.begin()+i,a.begin()+i+1);
        }
        else
        {
            x=a[i]-'0';
            for(j=1;j<=x;j++)
            {
                s.append(add_string);
            }
        }
    }
    ll ans = KMP_String_Matching().KMPSearch(b,s);
    cout<<ans<<endl;
}
