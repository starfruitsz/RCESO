# 附录 A 补充：2× 分量的来源（OMML 片段）

> 与报告附录 A.10 的 2× 来源一致；共 16 个式子。
> 用法：打开同目录「附录A_2x来源_公式_含平行不对中.docx」复制整条公式；或复制下面的 m:oMath 片段。
> 符号：β 角不对中；θ、ω 转角与角速度；a 平行偏移；k_x、k_y 联轴器两向刚度；S(s) 速度环灵敏度。

## 1 现有方程是通用的，2× 由 T(θ) 提供

### ① 绕轴转矩方程（对任意谐波成立）

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>I</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>n</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:acc>
    <m:accPr>
      <m:chr m:val="̇"/>
    </m:accPr>
    <m:e>
      <m:r>
        <m:t>ω</m:t>
      </m:r>
    </m:e>
  </m:acc>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>=</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>T</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>e</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>−</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>T</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>L</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:r>
    <m:t>θ</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>)</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>−</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>T</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>f</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:r>
    <m:t>θ</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>,</m:t>
  </m:r>
  <m:r>
    <m:t>ω</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>)</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>+</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>M</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>g</m:t>
      </m:r>
      <m:r>
        <m:t>Z</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:r>
    <m:t>θ</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>)</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>+</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>T</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>m</m:t>
      </m:r>
      <m:r>
        <m:t>i</m:t>
      </m:r>
      <m:r>
        <m:t>s</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:r>
    <m:t>θ</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>)</m:t>
  </m:r>
</m:oMath>
```

### ② 第 k 次谐波的转速纹波

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>Δ</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>ω</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>k</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>≈</m:t>
  </m:r>
  <m:d>
    <m:dPr>
      <m:begChr m:val="|"/>
      <m:sepChr m:val=""/>
      <m:endChr m:val="|"/>
      <m:grow/>
    </m:dPr>
    <m:e>
      <m:r>
        <m:t>S</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>(</m:t>
      </m:r>
      <m:r>
        <m:t>j</m:t>
      </m:r>
      <m:r>
        <m:t>k</m:t>
      </m:r>
      <m:r>
        <m:t>ω</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>)</m:t>
      </m:r>
    </m:e>
  </m:d>
  <m:f>
    <m:fPr>
      <m:type m:val="bar"/>
    </m:fPr>
    <m:num>
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>T</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>k</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
    </m:num>
    <m:den>
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>I</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>n</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
      <m:r>
        <m:t>k</m:t>
      </m:r>
      <m:r>
        <m:t>ω</m:t>
      </m:r>
    </m:den>
  </m:f>
</m:oMath>
```

## 2 来源一：Hooke / 十字滑块运动学

### ③ 两轴转角关系

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>tan</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>θ</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>2</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>=</m:t>
  </m:r>
  <m:f>
    <m:fPr>
      <m:type m:val="bar"/>
    </m:fPr>
    <m:num>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>tan</m:t>
      </m:r>
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>θ</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>1</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
    </m:num>
    <m:den>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>cos</m:t>
      </m:r>
      <m:r>
        <m:t>β</m:t>
      </m:r>
    </m:den>
  </m:f>
</m:oMath>
```

### ④ 从动轴角速度比

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:f>
    <m:fPr>
      <m:type m:val="bar"/>
    </m:fPr>
    <m:num>
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>ω</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>2</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
    </m:num>
    <m:den>
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>ω</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>1</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
    </m:den>
  </m:f>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>=</m:t>
  </m:r>
  <m:f>
    <m:fPr>
      <m:type m:val="bar"/>
    </m:fPr>
    <m:num>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>cos</m:t>
      </m:r>
      <m:r>
        <m:t>β</m:t>
      </m:r>
    </m:num>
    <m:den>
      <m:r>
        <m:t>1</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>−</m:t>
      </m:r>
      <m:sSup>
        <m:e>
          <m:r>
            <m:rPr>
              <m:sty m:val="p"/>
            </m:rPr>
            <m:t>sin</m:t>
          </m:r>
        </m:e>
        <m:sup>
          <m:r>
            <m:t>2</m:t>
          </m:r>
        </m:sup>
      </m:sSup>
      <m:r>
        <m:t>β</m:t>
      </m:r>
      <m:sSup>
        <m:e>
          <m:r>
            <m:rPr>
              <m:sty m:val="p"/>
            </m:rPr>
            <m:t>cos</m:t>
          </m:r>
        </m:e>
        <m:sup>
          <m:r>
            <m:t>2</m:t>
          </m:r>
        </m:sup>
      </m:sSup>
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>θ</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>1</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
    </m:den>
  </m:f>
</m:oMath>
```

### ⑤ 小角度展开（2× 项出现）

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:f>
    <m:fPr>
      <m:type m:val="bar"/>
    </m:fPr>
    <m:num>
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>ω</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>2</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
    </m:num>
    <m:den>
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>ω</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>1</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
    </m:den>
  </m:f>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>≈</m:t>
  </m:r>
  <m:r>
    <m:t>1</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>+</m:t>
  </m:r>
  <m:f>
    <m:fPr>
      <m:type m:val="bar"/>
    </m:fPr>
    <m:num>
      <m:sSup>
        <m:e>
          <m:r>
            <m:t>β</m:t>
          </m:r>
        </m:e>
        <m:sup>
          <m:r>
            <m:t>2</m:t>
          </m:r>
        </m:sup>
      </m:sSup>
    </m:num>
    <m:den>
      <m:r>
        <m:t>2</m:t>
      </m:r>
    </m:den>
  </m:f>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>cos</m:t>
  </m:r>
  <m:r>
    <m:t>2</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>θ</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>1</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
</m:oMath>
```

### ⑥ 恒功率下的转矩 2× 纹波

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>T</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>2</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>≈</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>T</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>1</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:d>
    <m:dPr>
      <m:begChr m:val="["/>
      <m:sepChr m:val=""/>
      <m:endChr m:val="]"/>
      <m:grow/>
    </m:dPr>
    <m:e>
      <m:r>
        <m:t>1</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>−</m:t>
      </m:r>
      <m:f>
        <m:fPr>
          <m:type m:val="bar"/>
        </m:fPr>
        <m:num>
          <m:sSup>
            <m:e>
              <m:r>
                <m:t>β</m:t>
              </m:r>
            </m:e>
            <m:sup>
              <m:r>
                <m:t>2</m:t>
              </m:r>
            </m:sup>
          </m:sSup>
        </m:num>
        <m:den>
          <m:r>
            <m:t>2</m:t>
          </m:r>
        </m:den>
      </m:f>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>cos</m:t>
      </m:r>
      <m:r>
        <m:t>2</m:t>
      </m:r>
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>θ</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>1</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
    </m:e>
  </m:d>
</m:oMath>
```

## 3 来源二：联轴器刚度各向异性

### ⑦ 弹性势能（偏移 a 在联轴器系中随 θ 转）

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:r>
    <m:t>U</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:r>
    <m:t>θ</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>)</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>=</m:t>
  </m:r>
  <m:f>
    <m:fPr>
      <m:type m:val="bar"/>
    </m:fPr>
    <m:num>
      <m:r>
        <m:t>1</m:t>
      </m:r>
    </m:num>
    <m:den>
      <m:r>
        <m:t>2</m:t>
      </m:r>
    </m:den>
  </m:f>
  <m:sSup>
    <m:e>
      <m:r>
        <m:t>a</m:t>
      </m:r>
    </m:e>
    <m:sup>
      <m:r>
        <m:t>2</m:t>
      </m:r>
    </m:sup>
  </m:sSup>
  <m:d>
    <m:dPr>
      <m:begChr m:val="("/>
      <m:sepChr m:val=""/>
      <m:endChr m:val=")"/>
      <m:grow/>
    </m:dPr>
    <m:e>
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>k</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>x</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
      <m:sSup>
        <m:e>
          <m:r>
            <m:rPr>
              <m:sty m:val="p"/>
            </m:rPr>
            <m:t>cos</m:t>
          </m:r>
        </m:e>
        <m:sup>
          <m:r>
            <m:t>2</m:t>
          </m:r>
        </m:sup>
      </m:sSup>
      <m:r>
        <m:t>θ</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>+</m:t>
      </m:r>
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>k</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>y</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
      <m:sSup>
        <m:e>
          <m:r>
            <m:rPr>
              <m:sty m:val="p"/>
            </m:rPr>
            <m:t>sin</m:t>
          </m:r>
        </m:e>
        <m:sup>
          <m:r>
            <m:t>2</m:t>
          </m:r>
        </m:sup>
      </m:sSup>
      <m:r>
        <m:t>θ</m:t>
      </m:r>
    </m:e>
  </m:d>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>=</m:t>
  </m:r>
  <m:f>
    <m:fPr>
      <m:type m:val="bar"/>
    </m:fPr>
    <m:num>
      <m:r>
        <m:t>1</m:t>
      </m:r>
    </m:num>
    <m:den>
      <m:r>
        <m:t>4</m:t>
      </m:r>
    </m:den>
  </m:f>
  <m:sSup>
    <m:e>
      <m:r>
        <m:t>a</m:t>
      </m:r>
    </m:e>
    <m:sup>
      <m:r>
        <m:t>2</m:t>
      </m:r>
    </m:sup>
  </m:sSup>
  <m:d>
    <m:dPr>
      <m:begChr m:val="["/>
      <m:sepChr m:val=""/>
      <m:endChr m:val="]"/>
      <m:grow/>
    </m:dPr>
    <m:e>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>(</m:t>
      </m:r>
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>k</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>x</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>+</m:t>
      </m:r>
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>k</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>y</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>)</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>+</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>(</m:t>
      </m:r>
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>k</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>x</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>−</m:t>
      </m:r>
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>k</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>y</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>)</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>cos</m:t>
      </m:r>
      <m:r>
        <m:t>2</m:t>
      </m:r>
      <m:r>
        <m:t>θ</m:t>
      </m:r>
    </m:e>
  </m:d>
</m:oMath>
```

### ⑧ 对 θ 的广义力矩

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>T</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>θ</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>=</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>−</m:t>
  </m:r>
  <m:f>
    <m:fPr>
      <m:type m:val="bar"/>
    </m:fPr>
    <m:num>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∂</m:t>
      </m:r>
      <m:r>
        <m:t>U</m:t>
      </m:r>
    </m:num>
    <m:den>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∂</m:t>
      </m:r>
      <m:r>
        <m:t>θ</m:t>
      </m:r>
    </m:den>
  </m:f>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>=</m:t>
  </m:r>
  <m:f>
    <m:fPr>
      <m:type m:val="bar"/>
    </m:fPr>
    <m:num>
      <m:sSup>
        <m:e>
          <m:r>
            <m:t>a</m:t>
          </m:r>
        </m:e>
        <m:sup>
          <m:r>
            <m:t>2</m:t>
          </m:r>
        </m:sup>
      </m:sSup>
    </m:num>
    <m:den>
      <m:r>
        <m:t>2</m:t>
      </m:r>
    </m:den>
  </m:f>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>k</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>x</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>−</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>k</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>y</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>)</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>sin</m:t>
  </m:r>
  <m:r>
    <m:t>2</m:t>
  </m:r>
  <m:r>
    <m:t>θ</m:t>
  </m:r>
</m:oMath>
```

### ⑨ 角不对中版本（a → β）

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>T</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>θ</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>=</m:t>
  </m:r>
  <m:f>
    <m:fPr>
      <m:type m:val="bar"/>
    </m:fPr>
    <m:num>
      <m:sSup>
        <m:e>
          <m:r>
            <m:t>β</m:t>
          </m:r>
        </m:e>
        <m:sup>
          <m:r>
            <m:t>2</m:t>
          </m:r>
        </m:sup>
      </m:sSup>
    </m:num>
    <m:den>
      <m:r>
        <m:t>2</m:t>
      </m:r>
    </m:den>
  </m:f>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>k</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>x</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>−</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>k</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>y</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>)</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>sin</m:t>
  </m:r>
  <m:r>
    <m:t>2</m:t>
  </m:r>
  <m:r>
    <m:t>θ</m:t>
  </m:r>
</m:oMath>
```

### ⑩ 本质：三角恒等式

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>cos</m:t>
  </m:r>
  <m:r>
    <m:t>θ</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>sin</m:t>
  </m:r>
  <m:r>
    <m:t>θ</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>=</m:t>
  </m:r>
  <m:f>
    <m:fPr>
      <m:type m:val="bar"/>
    </m:fPr>
    <m:num>
      <m:r>
        <m:t>1</m:t>
      </m:r>
    </m:num>
    <m:den>
      <m:r>
        <m:t>2</m:t>
      </m:r>
    </m:den>
  </m:f>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>sin</m:t>
  </m:r>
  <m:r>
    <m:t>2</m:t>
  </m:r>
  <m:r>
    <m:t>θ</m:t>
  </m:r>
</m:oMath>
```

## 4 来源三：间隙 / 接触非线性

### ⑪ 死区特性（傅里叶展开含 2×、3×）

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>T</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>g</m:t>
      </m:r>
      <m:r>
        <m:t>a</m:t>
      </m:r>
      <m:r>
        <m:t>p</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:r>
    <m:t>φ</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>)</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>=</m:t>
  </m:r>
  <m:d>
    <m:dPr>
      <m:begChr m:val="{"/>
      <m:sepChr m:val=""/>
      <m:endChr m:val=""/>
      <m:grow/>
    </m:dPr>
    <m:e>
      <m:m>
        <m:mPr>
          <m:baseJc m:val="center"/>
          <m:plcHide m:val="on"/>
          <m:mcs>
            <m:mc>
              <m:mcPr>
                <m:mcJc m:val="left"/>
                <m:count m:val="1"/>
              </m:mcPr>
            </m:mc>
            <m:mc>
              <m:mcPr>
                <m:mcJc m:val="left"/>
                <m:count m:val="1"/>
              </m:mcPr>
            </m:mc>
          </m:mcs>
        </m:mPr>
        <m:mr>
          <m:e>
            <m:r>
              <m:t>k</m:t>
            </m:r>
            <m:r>
              <m:rPr>
                <m:sty m:val="p"/>
              </m:rPr>
              <m:t>(</m:t>
            </m:r>
            <m:r>
              <m:t>φ</m:t>
            </m:r>
            <m:r>
              <m:rPr>
                <m:sty m:val="p"/>
              </m:rPr>
              <m:t>−</m:t>
            </m:r>
            <m:r>
              <m:t>g</m:t>
            </m:r>
            <m:r>
              <m:rPr>
                <m:sty m:val="p"/>
              </m:rPr>
              <m:t>)</m:t>
            </m:r>
            <m:r>
              <m:rPr>
                <m:sty m:val="p"/>
              </m:rPr>
              <m:t>,</m:t>
            </m:r>
          </m:e>
          <m:e>
            <m:r>
              <m:t>φ</m:t>
            </m:r>
            <m:r>
              <m:rPr>
                <m:sty m:val="p"/>
              </m:rPr>
              <m:t>&gt;</m:t>
            </m:r>
            <m:r>
              <m:t>g</m:t>
            </m:r>
          </m:e>
        </m:mr>
        <m:mr>
          <m:e>
            <m:r>
              <m:t>0</m:t>
            </m:r>
            <m:r>
              <m:rPr>
                <m:sty m:val="p"/>
              </m:rPr>
              <m:t>,</m:t>
            </m:r>
          </m:e>
          <m:e>
            <m:r>
              <m:rPr>
                <m:sty m:val="p"/>
              </m:rPr>
              <m:t>|</m:t>
            </m:r>
            <m:r>
              <m:t>φ</m:t>
            </m:r>
            <m:r>
              <m:rPr>
                <m:sty m:val="p"/>
              </m:rPr>
              <m:t>|</m:t>
            </m:r>
            <m:r>
              <m:rPr>
                <m:sty m:val="p"/>
              </m:rPr>
              <m:t>≤</m:t>
            </m:r>
            <m:r>
              <m:t>g</m:t>
            </m:r>
          </m:e>
        </m:mr>
        <m:mr>
          <m:e>
            <m:r>
              <m:t>k</m:t>
            </m:r>
            <m:r>
              <m:rPr>
                <m:sty m:val="p"/>
              </m:rPr>
              <m:t>(</m:t>
            </m:r>
            <m:r>
              <m:t>φ</m:t>
            </m:r>
            <m:r>
              <m:rPr>
                <m:sty m:val="p"/>
              </m:rPr>
              <m:t>+</m:t>
            </m:r>
            <m:r>
              <m:t>g</m:t>
            </m:r>
            <m:r>
              <m:rPr>
                <m:sty m:val="p"/>
              </m:rPr>
              <m:t>)</m:t>
            </m:r>
            <m:r>
              <m:rPr>
                <m:sty m:val="p"/>
              </m:rPr>
              <m:t>,</m:t>
            </m:r>
          </m:e>
          <m:e>
            <m:r>
              <m:t>φ</m:t>
            </m:r>
            <m:r>
              <m:rPr>
                <m:sty m:val="p"/>
              </m:rPr>
              <m:t>&lt;</m:t>
            </m:r>
            <m:r>
              <m:rPr>
                <m:sty m:val="p"/>
              </m:rPr>
              <m:t>−</m:t>
            </m:r>
            <m:r>
              <m:t>g</m:t>
            </m:r>
          </m:e>
        </m:mr>
      </m:m>
    </m:e>
  </m:d>
</m:oMath>
```

## 5 代回纹波公式

### ⑫ 2× 转速纹波

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>Δ</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>ω</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>2</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>≈</m:t>
  </m:r>
  <m:d>
    <m:dPr>
      <m:begChr m:val="|"/>
      <m:sepChr m:val=""/>
      <m:endChr m:val="|"/>
      <m:grow/>
    </m:dPr>
    <m:e>
      <m:r>
        <m:t>S</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>(</m:t>
      </m:r>
      <m:r>
        <m:t>j</m:t>
      </m:r>
      <m:r>
        <m:t>2</m:t>
      </m:r>
      <m:r>
        <m:t>ω</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>)</m:t>
      </m:r>
    </m:e>
  </m:d>
  <m:f>
    <m:fPr>
      <m:type m:val="bar"/>
    </m:fPr>
    <m:num>
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>T</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>2</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
    </m:num>
    <m:den>
      <m:r>
        <m:t>2</m:t>
      </m:r>
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>I</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>n</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
      <m:r>
        <m:t>ω</m:t>
      </m:r>
    </m:den>
  </m:f>
</m:oMath>
```

## 6 平行不对中：几何与 2× 转矩

### ⑬ 平行偏移矢量（空间固定，随 θ 旋转）

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:r>
    <m:rPr>
      <m:sty m:val="bi"/>
    </m:rPr>
    <m:t>e</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:r>
    <m:t>θ</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>)</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>=</m:t>
  </m:r>
  <m:d>
    <m:dPr>
      <m:begChr m:val="("/>
      <m:sepChr m:val=""/>
      <m:endChr m:val=")"/>
      <m:grow/>
    </m:dPr>
    <m:e>
      <m:r>
        <m:t>e</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>cos</m:t>
      </m:r>
      <m:r>
        <m:t>θ</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>,</m:t>
      </m:r>
      <m:r>
        <m:t> </m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>−</m:t>
      </m:r>
      <m:r>
        <m:t>e</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>sin</m:t>
      </m:r>
      <m:r>
        <m:t>θ</m:t>
      </m:r>
    </m:e>
  </m:d>
</m:oMath>
```

### ⑭ 恒定径向力（各向同性时唯一效果）

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:r>
    <m:rPr>
      <m:sty m:val="bi"/>
    </m:rPr>
    <m:t>F</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>=</m:t>
  </m:r>
  <m:r>
    <m:t>k</m:t>
  </m:r>
  <m:r>
    <m:t> </m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="bi"/>
    </m:rPr>
    <m:t>e</m:t>
  </m:r>
</m:oMath>
```

### ⑮ 弹性势能（各向异性）

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:r>
    <m:t>U</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:r>
    <m:t>θ</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>)</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>=</m:t>
  </m:r>
  <m:f>
    <m:fPr>
      <m:type m:val="bar"/>
    </m:fPr>
    <m:num>
      <m:r>
        <m:t>1</m:t>
      </m:r>
    </m:num>
    <m:den>
      <m:r>
        <m:t>2</m:t>
      </m:r>
    </m:den>
  </m:f>
  <m:sSup>
    <m:e>
      <m:r>
        <m:t>e</m:t>
      </m:r>
    </m:e>
    <m:sup>
      <m:r>
        <m:t>2</m:t>
      </m:r>
    </m:sup>
  </m:sSup>
  <m:d>
    <m:dPr>
      <m:begChr m:val="("/>
      <m:sepChr m:val=""/>
      <m:endChr m:val=")"/>
      <m:grow/>
    </m:dPr>
    <m:e>
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>k</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>x</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
      <m:sSup>
        <m:e>
          <m:r>
            <m:rPr>
              <m:sty m:val="p"/>
            </m:rPr>
            <m:t>cos</m:t>
          </m:r>
        </m:e>
        <m:sup>
          <m:r>
            <m:t>2</m:t>
          </m:r>
        </m:sup>
      </m:sSup>
      <m:r>
        <m:t>θ</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>+</m:t>
      </m:r>
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>k</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>y</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
      <m:sSup>
        <m:e>
          <m:r>
            <m:rPr>
              <m:sty m:val="p"/>
            </m:rPr>
            <m:t>sin</m:t>
          </m:r>
        </m:e>
        <m:sup>
          <m:r>
            <m:t>2</m:t>
          </m:r>
        </m:sup>
      </m:sSup>
      <m:r>
        <m:t>θ</m:t>
      </m:r>
    </m:e>
  </m:d>
</m:oMath>
```

### ⑯ 绕轴 2× 转矩（各向同性时为零）

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>T</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>θ</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>=</m:t>
  </m:r>
  <m:f>
    <m:fPr>
      <m:type m:val="bar"/>
    </m:fPr>
    <m:num>
      <m:sSup>
        <m:e>
          <m:r>
            <m:t>e</m:t>
          </m:r>
        </m:e>
        <m:sup>
          <m:r>
            <m:t>2</m:t>
          </m:r>
        </m:sup>
      </m:sSup>
    </m:num>
    <m:den>
      <m:r>
        <m:t>2</m:t>
      </m:r>
    </m:den>
  </m:f>
  <m:d>
    <m:dPr>
      <m:begChr m:val="("/>
      <m:sepChr m:val=""/>
      <m:endChr m:val=")"/>
      <m:grow/>
    </m:dPr>
    <m:e>
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>k</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>x</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>−</m:t>
      </m:r>
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>k</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>y</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
    </m:e>
  </m:d>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>sin</m:t>
  </m:r>
  <m:r>
    <m:t>2</m:t>
  </m:r>
  <m:r>
    <m:t>θ</m:t>
  </m:r>
</m:oMath>
```

---

说明：LaTeX 源在 _appx2x_math.md，docx 由 pandoc 生成，OMML 已清理命名空间；MathType 可直接识别 docx 里的公式。