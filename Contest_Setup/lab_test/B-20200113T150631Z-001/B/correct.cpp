#include <bits/stdc++.h>
using namespace std;

int main() {
  freopen("input02.in","r",stdin);
  freopen("output02.ans","w",stdout);
  int W, H, N;
  cin >> W >> H >> N;
  vector<vector<int>> field(H, vector<int>(W, 0));

  for (int i = 0; i < N; i++) {
    int x, y, a;
    cin >> x >> y >> a;

    if (a == 1) {
      for (int i = 0; i < H; i++) {
        for (int j = 0; j < x; j++) {
          field.at(i).at(j) = 1;
        }
      }
    }
    else if (a == 2) {
      for (int i = 0; i < H; i++) {
        for (int j = x; j < W; j++) {
          field.at(i).at(j) = 1;
        }
      }
    }
    else if (a == 3) {
      for (int i = 0; i < y; i++) {
        for (int j = 0; j < W; j++) {
          field.at(i).at(j) = 1;
        }
      }
    }
    else if (a == 4) {
      for (int i = y; i < H; i++) {
        for (int j = 0; j < W; j++) {
          field.at(i).at(j) = 1;
        }
      }
    }
  }

  int cnt = 0;
  for (int i = 0; i < H; i++) {
    for (int j = 0; j < W; j++) {
      if (field.at(i).at(j) == 0) cnt++;
    }
  }
  cout << cnt << endl;

}
