#include <bits/stdc++.h>

using namespace std;


int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(0);
  freopen("input05.in","r",stdin);
    freopen("output05.ans","w",stdout);
  int n;
  cin >> n;
  vector<int> a(n + n - 1);
  for (int i = 0; i < n + n - 1; i++) {
    cin >> a[i];
    a[i]--;
  }
  auto ok = [&](int mid) {
    int alt_left = 0, alt_right = 0;
    for (int j = n - 1; j - 1 >= 0 && (a[j] >= mid) != (a[j - 1] >= mid); j--) {
      alt_left++;
    }
    for (int j = n - 1; j + 1 < n + n - 1 && (a[j] >= mid) != (a[j + 1] >= mid); j++) {
      alt_right++;
    }
    return (a[n - 1] >= mid) ^ (min(alt_left, alt_right) & 1);
  };
  int low = 0, high = n + n - 1, mid;
  while (low < high) {
    mid = (low + high + 1) >> 1;
    if (ok(mid)) {
      low = mid;
    } else {
      high = mid - 1;
    }
  }
  cout << low + 1 << '\n';
  return 0;
}
