# KO1KEYZ公式コンセプトフォトからメンバー写真を切り出す方法(2026-09-05判明)

私物・イベントレポなど「メンバー本人の写真を1枚だけ添えたい」場面で使える、安全な写真ソース。オフライントーク会など会場での撮影が禁止されているイベントのレポ記事では特に有用。

## 元ネタ

2026-08-02前後にXで拡散された「【KO1KEYZ CONCEPT PHOTO】」コラージュ画像2枚(各メンバーのデビュー記念コンセプトフォト、公式配布素材の二次拡散)。`tools/Xiy/posts_20260802_member_<英字名>/images/post_4_img_1.jpg`・`post_4_img_2.jpg`として、12人分すべての個人フォルダに同じ画像が重複保存されている。

## レイアウト

2048×1407pxの画像2枚、それぞれ3列×2行(6人分)のグリッド。**メンバーの並び順は名前コール順(活動名アルファベット順)と完全に一致**:

- **1枚目**(`post_4_img_1.jpg`): 1.DAIKI(左上) → 2.ISSA(中上) → 3.KEITO(右上) → 4.KOSUKE(左下) → 5.RYOGA(中下) → 6.RYUJI(右下)
- **2枚目**(`post_4_img_2.jpg`): 7.SHINHAENG(左上) → 8.SIYOUNG(中上) → 9.TOWA(右上) → 10.YOSHIKI(左下) → 11.YUKI(中下) → 12.YURA(右下)

名前コール順の出典は[[ko1keyz-1st-fanmeeting-schedule]]と同じ`lapone-4groups-namecall-spec.md`。

## 切り出し方(PILで機械的に3分割×2分割)

```python
from PIL import Image
im = Image.open("tools/Xiy/posts_20260802_member_<名前>/images/post_4_img_2.jpg")
w, h = im.size
# 例: 2枚目・中上(SIYOUNG=8番目)
crop = im.crop((int(w/3), 0, int(2*w/3), int(h*0.5)))
crop.save("images/<name>_concept_photo.jpg")
```

x方向は`[0, w/3, 2w/3, w]`で列を、y方向は`[0, h/2, h]`で行を区切るだけで各メンバーの升目に当たる。境界に細い色枠があるので多少ズレても実害はない。

## 裏取りの手順(思い込みで断定しない)

名前コール順だけで決め打ちせず、メンバー個別フォルダ内の別投稿(本人のハッシュタグ・メンバーカラーへの言及がある投稿)の写真と衣装・顔を見比べて同一人物か必ず確認すること(2026-09-05にYOSHIKI=ピンク髪の一致・SIYOUNG=赤黒ボーダーシャツで別投稿と一致を確認して採用した実績あり)。[[feedback_dont_guess_member_identity_from_video_frames]]と同じ理由で、機械的な位置合わせだけを根拠に本文へ使わない。

## 使い所

- 公式コンセプトフォトなので肖像権・イベント撮影禁止のリスクを避けられる
- キャプションは「出典:元ツイートURL(コンセプトフォトの二次拡散)」で明記する
