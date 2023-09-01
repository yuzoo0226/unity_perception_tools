# Unityでデータセットの生成手法
- Unityはかなり容量を食うので，インストール前に空き容量を確認すること

## 実験環境
- Ubuntu 16.04
- Unity2019.4.29f1

## Unity install
- ~/Unity にUnityのプログラムをinstallする
- UnityをUbuntuにinstallする方法は[この](http://pineplanter.moo.jp/non-it-salaryman/2020/08/09/unity-ubuntu/)サイトの通りに行いました

- [UnityHub.Appimage](https://drive.google.com/file/d/1uMzaFg1zfI7J_3nsF0m51sLvDlfnE82v/view?usp=sharing)をダウンロードする
- monoのinstallについては，ubuntuのversionに応じて変更する必要が有ります
- Ubuntuのverごとのコマンドに関しては，[この](https://www.mono-project.com/download/stable/#download-lin)サイトにまとまっています

## Unity環境設定
```
### new terminal ###
cd ~
cd Unity
git clone https://github.com/Unity-Technologies/com.unity.perception.git
```
## プロジェクト作成・起動
- Unityを起動してプロジェクトタブを開く
- リストに追加を選択し，gitからcloneした「com.unity.perception/Testprojects/Perception**HDRP**」を選択しOKを押す

## アノテーションのテストまで
### Perceptionモジュールのimport
- 左上のメニューから「window＞Package Manager」を選択</br>
![Screenshot from 2021-08-11 00-52-11.png](/attachment/6112a15015adcd006e425c8a)
- 左上の`＋`から，`Add Package from git URL`を選択し，検索ボックスに`com.unity.perception`と入力しEnter
- `Perception`というタブが追加されているので開き，2つともimportする（画像はimport後）</br>
![Screenshot from 2021-08-11 00-55-27.png](/attachment/6112a24f15adcd006e425c90)

### Mein Cameraの設定
- `Hierarchy`(左側にあるメニュー)から`Mein Camera`を選択すると，右に`Inspector`が表示される
- 下部にある，`Add Component`を選択し，検索ボックスに「Perception Camera」を入力し追加する
- `Camera Labels`を下の写真のようにする
   - `IdLabelConfig`と`semanticsegmentationLabelingConfig`が見つからない場合に考えられること
      - HDRPではなくURPを選択している可能性あり
      - HDRPのAssetsの中にあるIdLabelConfigをURP内にもコピーすることで使用できる</br>
![Screenshot from 2021-08-11 00-58-47.png](/attachment/6112a41615adcd006e425c95)

### Label Config
- ProjectフォルダのAssetsを選択
- `IdLabelConfig`を選択すると，右側に下の写真のような画面が出るので，このようにセットする</br>
![IDLabelconfig.png](/attachment/611414f015adcd006e425d35)
- 認識したい物体のLabelをAdd new Labelを使って追加する（今回は特に目的はないが全て追加する）
- `SemanticSegmentationLabelingConfigration`も同様にして，以下のように設定する</br>
![Screenshot from 2021-08-12 03-13-05.png](/attachment/6114158115adcd006e425d3a)

### Test
- 左下のProjectから</bn>
「Samples/Perception/0.8.0.../Tutolial Files/Foreground Objects/Phase1/Models」に移動し，適当なオブジェクトをカメラに映る位置に配置する
- カメラ座標をxyzすべて0にして，配置した物体の座標をx=1, y=0, z=2にすると映る位置に来る
   - 複数配置したい場合は，xの位置を-2~2の範囲で移動させてみるのが無難
- カメラに物体が映ることを確認したら,上の中央部にあるGameタブを選択し，▶を押す
- ここまできちんと出来ていたら，アノテーションを行ったものが得られるはず！！！</br>
![Screenshot from 2021-08-11 01-17-05.png](/attachment/6112a7e915adcd006e425c9f)
- 注意：対応色はこの結果と異なっている場合が有ります

## ランダム配置・カメラ配置ランダム化(そのうち日本語化します)
- Action: Create a new GameObject in your Scene by right-clicking in the Hierarchy tab and clicking Create Empty.
- Action: Rename your new GameObject to Simulation Scenario.
- Action: In the Inspector view of this new object, add a new Fixed Length Scenario component.

- Action: Add `ForegroundObjectPlacementRandomizer` to your list of Randomizers. Click Add Folder and select `Assets/Samples/Perception/0.8.0-preview.1/Tutorial Files/Foreground Objects/Phase 1/Prefabs`.
- Action: Set these values for the above Randomizer: `Depth = -3, Separation Distance = 1.5, Placement Area = (5,5)`.
- Action: From the Project tab select all the foreground Prefabs located in `Assets/Samples/Perception/0.8.0-preview.1/Tutorial Files/Foreground Objects/Phase 1/Prefabs`, and add a RotationRandomizerTag component to them.
- Action: Drag ForegroundObjectPlacementRandomizer using the striped handle bar (on its left side) and drop it above RotationRandomizer.
- Action Click ▷ (play) again and this time let the simulation finish. This should take only a few seconds.

## 画像保存・アノテーションデータ保存
- 上にまとめた


# 結果
----------------------
| RGB                                                | Segmentation                                                |
| -------------------------------------------------- | ----------------------------------------------------------- |
| ![rgb_2.png](/attachment/6114184e15adcd006e425d5f) | ![segmentation_2.png](/attachment/6114186215adcd006e425d67) |
| ![rgb_5.png](/attachment/6114187b15adcd006e425d71) | ![segmentation_5.png](/attachment/6114189815adcd006e425d7f) |

# 参考文献
- [Unityでのデータセット生成手順（これが一番わかり易いです）](https://github.com/Unity-Technologies/com.unity.perception/blob/master/com.unity.perception/Documentation~/Tutorial/Phase1.md)
- [Unityでディープラーニング学習用の教師データを大量に生成する方法](https://zenn.dev/karaage0703/articles/2d54b5c02dfe39)
- [git project](https://github.com/Unity-Technologies/com.unity.perception)


# Unity 地形生成

### 動作環境
- Ubuntu 16.04
- Unity 19.04.24f

# 起伏のある地形作成
- 新規の3Dプロジェクト作成（名前は任意）

## 地形オブジェクトの作成
### Prefabデータ作成
- `Hierarchy`から`3DObject`→`Cube`の順に選択
- 作成したCubeの名称を`Field Cell`に変更
- `Transform`の`Scale`を変更する
   - Y = 10
- 作成したCubeをPrefab化する（[Prefab作成方法](https://xr-hub.com/archives/11132)）
- Prefab化まで完了したら，作成したCubeオブジェクトは削除する

### スクリプトの作成
- 以下のコードをコピペして自分のプロジェクトフォルダに追加する
   - （自分は，`Assets`フォルダの下に`Scripts`というフォルダを作成し，そこに作成していく）
   - ファイル名は`FieldGenerator`にする（変更したい場合は，下記プログラムのclass名を変更する必要あり）

```
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

/// <Summary>
/// パーリンノイズを使ってフィールドを生成するクラスです。
/// </Summary>
public class FieldGenerator : MonoBehaviour
{
    // フィールド作成のためのパーツへの参照です。
    public GameObject fieldParts;

    // フィールドパーツの親オブジェクトのTransformです。
    public Transform fieldParent;

    // フィールドに関する情報です。
    public int fieldSizeX = 50;
    public int fieldSizeZ = 50;
    public int fieldHeight = 50;

    // パーリンノイズに関する情報です。
    public float xOrigin;
    public float yOrigin;
    public float scale = 0.01f;


    void Start()
    {

    }

    void Update()
    {

    }

    /// <Summary>
    /// 生成ボタンが押された時のメソッドです。
    /// </Summary>
    public void OnPressedGenerateButton()
    {
        GenerateFieldParts();
    }

    /// <Summary>
    /// フィールドを生成するメソッドです。
    /// </Summary>
    void GenerateFieldParts()
    {
        for (float z = 0f; z < fieldSizeZ; z++)
        {
            for (float x = 0f; x < fieldSizeX; x++)
            {
                // パーリンノイズの座標を指定して値を取得します。
                float xValue = xOrigin + x * scale;
                float yValue = yOrigin + z * scale;
                float perlinValue = Mathf.PerlinNoise(xValue, yValue);
                float height = fieldHeight * perlinValue;

                // 位置のVector3を作成してオブジェクトをインスタンス化します。
                Vector3 pos = new Vector3(x, height, z);
                InstantiateFieldParts(pos);
            }
        }
    }

    /// <Summary>
    /// オブジェクトをインスタンス化するメソッドです。
    /// </Summary>
    void InstantiateFieldParts(Vector3 pos)
    {
        // オブジェクトをインスタンス化します。
        GameObject obj = Instantiate(fieldParts, Vector3.zero, Quaternion.identity);

        // オブジェクトのTransformを設定します。
        obj.transform.SetParent(fieldParent);
        obj.transform.localPosition = pos;
    }

    /// <Summary>
    /// 削除ボタンが押された時のメソッドです。
    /// </Summary>
    public void OnPressedRemoveButton()
    {
        RemoveFieldParts();
    }

    /// <Summary>
    /// フィールドのパーツを削除するメソッドです。
    /// </Summary>
    void RemoveFieldParts()
    {
        foreach (Transform tran in fieldParent)
        {
            Destroy(tran.gameObject);
        }
    }
}
```

- `Field Parts`を`FieldCell(作成した3DCube)`に設定
- 次に`Create Empty`でGameoBjectを1つ作成し，名称を`FieldParent`とする

### ボタンの設定
#### ボタンの作成
- `UI`→`Button`からオブジェクトボタンを作成する(親オブジェクトとして作成する)

#### スクリプトの有効化
- 先ほど作成したスクリプトを，`Hierarchy`の`Button`にドラッグアンドドロップする
- ![Screenshot from 2021-08-23 17-47-44.png](/attachment/6123619615adcd006e4261ba)
- このようになれば成功
- OnClick()のところにある＋を選択
- `None(Object)`となっているところに，`Hierarchy`のButtonをドラッグ・アンド・ドロップする
- ![Screenshot from 2021-08-23 17-51-41.png](/attachment/6123624315adcd006e4261bf)
- このようになれば成功
- `No Function`となっているところをクリックし，`FieldGenerator`→`OnPressedGenerateButton`を選択

### 地形作成のテスト
- ここまで完成したら，上部の▶をクリックし，gameモードに移行
- `Button`をクリックし，何かしら出てきたら成功

#### パラメータ調整
- パラメータは`Hierarchy`の`Button`から`Field Generator（Script）`を編集する
- Field Sizeを変更すると大きさが変わる
- Field Hightは高さが変わる
- Scaleは一個あたりのオブジェクトの大きさが変わる
- 今回の設定

```
Size(x, z) = (500, 500)
Scale = 0.03
MainCamera = Pos(150, 150, -10)  Rot(40, 0, 0) Scale(1, 1, 1)
```
- こんな感じになる
![Screenshot from 2021-08-23 18-54-57.png](/attachment/6123712a15adcd006e4261c8)


