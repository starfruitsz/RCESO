# 附录 A 补充：三部分公式（OMML 片段）

> 与报告附录 A.7–A.9（rcso_v3.tex）一致，共 11 个式子。
> 用法：打开同目录「附录A_三部分_公式.docx」直接复制整条公式；或复制下面的 m:oMath 片段。
> 符号：β 角不对中；θ、ω 转角与机械角速度；I_p、I_t 极/赤道惯量；I_n = I_t sin²β + I_p cos²β；
> m、l、d = l sinβ；a、b、L = a+b 轴承位置与跨距；μ_b、r_b 轴承摩擦系数/半径；c_v 粘性阻尼；S(s) 速度环灵敏度。

## 1 轴承反力（力平衡 + 力矩平衡）

### ① 质心向心加速度

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>a</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>C</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>M</m:t>
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
  <m:sSup>
    <m:e>
      <m:r>
        <m:t>ω</m:t>
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
        <m:t>r</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>⟂</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
</m:oMath>
```

### ② 力平衡

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:r>
    <m:t>m</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>a</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>C</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>M</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>=</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>R</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>A</m:t>
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
        <m:t>R</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>B</m:t>
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
        <m:t>F</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>g</m:t>
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
        <m:t>F</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>c</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>o</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>u</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>p</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:t> </m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>⇒</m:t>
  </m:r>
  <m:r>
    <m:t> </m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>R</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>A</m:t>
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
        <m:t>R</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>B</m:t>
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
  <m:r>
    <m:t>m</m:t>
  </m:r>
  <m:sSup>
    <m:e>
      <m:r>
        <m:t>ω</m:t>
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
        <m:t>r</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>⟂</m:t>
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
        <m:t>F</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>g</m:t>
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
        <m:t>F</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>c</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>o</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>u</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>p</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>≡</m:t>
  </m:r>
  <m:r>
    <m:t>F</m:t>
  </m:r>
</m:oMath>
```

### ③ 对 O 点力矩平衡（两轴承 r_A = −aẐ、r_B = +bẐ）

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>r</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>A</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>×</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>R</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>A</m:t>
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
        <m:t>r</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>B</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>×</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>R</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>B</m:t>
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
    <m:t>ω</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>×</m:t>
  </m:r>
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
            <m:t>J</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>O</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
      <m:r>
        <m:t>ω</m:t>
      </m:r>
    </m:e>
  </m:d>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>−</m:t>
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
        <m:t>M</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>c</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>o</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>u</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>p</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>≡</m:t>
  </m:r>
  <m:r>
    <m:t>N</m:t>
  </m:r>
</m:oMath>
```

### ④ 投影到 ⊥Z 平面

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:r>
    <m:t>a</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>R</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>A</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>−</m:t>
  </m:r>
  <m:r>
    <m:t>b</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>R</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>B</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>=</m:t>
  </m:r>
  <m:acc>
    <m:accPr>
      <m:chr m:val="̂"/>
    </m:accPr>
    <m:e>
      <m:r>
        <m:t>Z</m:t>
      </m:r>
    </m:e>
  </m:acc>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>×</m:t>
  </m:r>
  <m:r>
    <m:t>N</m:t>
  </m:r>
</m:oMath>
```

### ⑤ 两轴承径向反力

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>R</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>A</m:t>
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
        <m:t>b</m:t>
      </m:r>
      <m:r>
        <m:t>F</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>+</m:t>
      </m:r>
      <m:acc>
        <m:accPr>
          <m:chr m:val="̂"/>
        </m:accPr>
        <m:e>
          <m:r>
            <m:t>Z</m:t>
          </m:r>
        </m:e>
      </m:acc>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>×</m:t>
      </m:r>
      <m:r>
        <m:t>N</m:t>
      </m:r>
    </m:num>
    <m:den>
      <m:r>
        <m:t>a</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>+</m:t>
      </m:r>
      <m:r>
        <m:t>b</m:t>
      </m:r>
    </m:den>
  </m:f>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>,</m:t>
  </m:r>
  <m:r>
    <m:t>  </m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>R</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>B</m:t>
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
        <m:t>a</m:t>
      </m:r>
      <m:r>
        <m:t>F</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>−</m:t>
      </m:r>
      <m:acc>
        <m:accPr>
          <m:chr m:val="̂"/>
        </m:accPr>
        <m:e>
          <m:r>
            <m:t>Z</m:t>
          </m:r>
        </m:e>
      </m:acc>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>×</m:t>
      </m:r>
      <m:r>
        <m:t>N</m:t>
      </m:r>
    </m:num>
    <m:den>
      <m:r>
        <m:t>a</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>+</m:t>
      </m:r>
      <m:r>
        <m:t>b</m:t>
      </m:r>
    </m:den>
  </m:f>
</m:oMath>
```

## 2 轴承摩擦转矩

### ⑥ 摩擦转矩模型

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
        <m:t>f</m:t>
      </m:r>
      <m:r>
        <m:t>0</m:t>
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
        <m:t>μ</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>b</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>r</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>b</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:d>
    <m:dPr>
      <m:begChr m:val="("/>
      <m:sepChr m:val=""/>
      <m:endChr m:val=")"/>
      <m:grow/>
    </m:dPr>
    <m:e>
      <m:d>
        <m:dPr>
          <m:begChr m:val="|"/>
          <m:sepChr m:val=""/>
          <m:endChr m:val="|"/>
          <m:grow/>
        </m:dPr>
        <m:e>
          <m:sSub>
            <m:e>
              <m:r>
                <m:t>R</m:t>
              </m:r>
            </m:e>
            <m:sub>
              <m:r>
                <m:t>A</m:t>
              </m:r>
            </m:sub>
          </m:sSub>
        </m:e>
      </m:d>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>+</m:t>
      </m:r>
      <m:d>
        <m:dPr>
          <m:begChr m:val="|"/>
          <m:sepChr m:val=""/>
          <m:endChr m:val="|"/>
          <m:grow/>
        </m:dPr>
        <m:e>
          <m:sSub>
            <m:e>
              <m:r>
                <m:t>R</m:t>
              </m:r>
            </m:e>
            <m:sub>
              <m:r>
                <m:t>B</m:t>
              </m:r>
            </m:sub>
          </m:sSub>
        </m:e>
      </m:d>
    </m:e>
  </m:d>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>+</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>c</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>v</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:t>ω</m:t>
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
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>c</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>a</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>g</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>e</m:t>
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

### ⑦ 载荷相关项的一阶展开

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:d>
    <m:dPr>
      <m:begChr m:val="|"/>
      <m:sepChr m:val=""/>
      <m:endChr m:val="|"/>
      <m:grow/>
    </m:dPr>
    <m:e>
      <m:r>
        <m:t>R</m:t>
      </m:r>
    </m:e>
  </m:d>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>≈</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>R</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>0</m:t>
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
        <m:t>R</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>1</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>cos</m:t>
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
    <m:t>−</m:t>
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
    <m:t> </m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>⇒</m:t>
  </m:r>
  <m:r>
    <m:t> </m:t>
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
      <m:r>
        <m:t>1</m:t>
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
        <m:t>μ</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>b</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>r</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>b</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>R</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>1</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>cos</m:t>
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
    <m:t>−</m:t>
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
</m:oMath>
```

## 3 绕轴转矩方程与转速纹波

### ⑧ 实际轴等效惯量

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
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>=</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>I</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>t</m:t>
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
    <m:t>β</m:t>
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
        <m:t>I</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>p</m:t>
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
    <m:t>β</m:t>
  </m:r>
</m:oMath>
```

### ⑨ 绕轴转矩方程

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
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>m</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>i</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
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

### ⑩ 第 k 次谐波的开环转速纹波

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
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>sin</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:r>
    <m:t>k</m:t>
  </m:r>
  <m:r>
    <m:t>θ</m:t>
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
        <m:t>ψ</m:t>
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
    <m:t>)</m:t>
  </m:r>
</m:oMath>
```

### ⑪ 计入速度环灵敏度 S(s) 的转速纹波

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

---

说明：11 个式子的 LaTeX 源在 _appx_math.md，docx 由 pandoc 生成，OMML 已做命名空间清理；
MathType 可直接识别 docx 里的公式，也可用 MathType 的 Toggle TeX 从 _appx_math.md 的 LaTeX 转入。