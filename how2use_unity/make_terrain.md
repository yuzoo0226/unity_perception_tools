# Unity 地形生成

## 動作環境

- Ubuntu 16.04
- Unity 19.04.24f

## 起伏のある地形作成

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

```C#
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

```bash
Size(x, z) = (500, 500)
Scale = 0.03
MainCamera = Pos(150, 150, -10)  Rot(40, 0, 0) Scale(1, 1, 1)
```

- こんな感じになる
![Screenshot from 2021-08-23 18-54-57.png](/attachment/6123712a15adcd006e4261c8)

### Potholeの配置

#### 標高に応じたオブジェクト配置

- 結局標高に応じて配置するわけではない
- pothole用のオブジェクトとして，直方体を設置する（名称はわかりやすくCratetrとした）
  - (以降は`Pothole`はアノテーション用のPotholeオブジェクトを示す)
- 画面表示は標高が高いものが優先されるので，`Y=n`（n=いい感じの値） の高さに設置する
- （Pothole部分としたいところはPothole用オブジェクトのほうが上にきて，それ以外は自動生成したFieldが上に来る）

#### オブジェクトの透明化

- Potholeを透明化する．
- Projectフォルダ内で，`Assets`フォルダに`Models`フォルダを作成する
- `Models`フォルダ内で，右クリック→`Create`→`Material`を選択
- `Surface Type`という項目を，`Opaque`**以外**にする
- `Base Map`という項目の横に，色を指定できそうなところがあるのでクリック
- 別Windowが開き，その下の方で`RGBA`の色指定を行えるので，Aを0にする（RGBはなんでもいい）
- 最終的にこうなっていれば成功（名称はTransparentに設定）
  - ![Screenshot from 2021-08-24 23-42-18.png]()
- PotholeにこのMaterialを適用する
- Potholeの`Inspector → Mesh Renderer → Element 0`に先ほど作成したTransparentを適用

## データアノテーション

- ここまでやるとできること

---------------------------
| RGB | anotation |
| --- | --------- |
| sample  | sample  |

## 参考文献

[パーリンノイズを使った地形を作るサンプル【エディタ拡張編】](https://ekulabo.com/unity-mesh-combine-on-editor)
