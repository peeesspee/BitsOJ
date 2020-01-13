#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main(){
    freopen("input01.in","r",stdin);
    freopen("output01.ans","w",stdout);
    int N;
    cin >> N;
    ll a[2 * N];

    for(int i = 0; i < 2 * N; ++i) cin >> a[i];
    sort(a, a + 2 * N);

    ll res = 0;
    for(int i = 2*N -1 ; i >= N; i--) res += a[i];

    cout << res << endl;
}
