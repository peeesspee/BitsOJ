#include <bits/stdc++.h>

using namespace std;

typedef long long ll;

const int N = 1e8;
const int INF = 1e9;
const int MOD = 998244353;


ll calc(string s) {

    ll ans = 0, cur = 0;
    for (int i = 0; i < s.size(); i++) {
        if (s[i] == '+') {
            ans += cur;
            cur = 0;
        }
        else
            cur = cur * 10 + (s[i] - '0');
    }
    return ans + cur;
}

int main() {
    freopen("input04.in","r",stdin);
    freopen("output04.ans","w",stdout);
    string s;
    cin >> s;
    int n = s.size();
    ll ans = 0;
    for (int msk = 0; msk < (1 << (n - 1)); msk++) {
        string t = "";
        for (int i = 0; i < n - 1; i++) {
            t += s[i];
            if (msk & (1 << i))
                t += '+';
        }
        t += s[n - 1];
        ans += calc(t);
    }
    cout << ans;
}
