# 附录 D：律 D / J / T 的稳定性与有界性（含 A5 证明 + L∞ 增益推导，OMML 片段）

> 共 38 个式子；D.2.1 第四步拆成 (a) L∞ 增益 与 (b) RC 小增益闭合。
> 用法：打开同目录「附录D_三律稳定性_含A5与L∞增益_v2.docx」复制整条公式；或复制下面的 m:oMath 片段。

## D.1 符号与模型

### ① 对象与控制律

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:acc>
    <m:accPr>
      <m:chr m:val="̇"/>
    </m:accPr>
    <m:e>
      <m:r>
        <m:t>x</m:t>
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
        <m:t>b</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>0</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:t>u</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>+</m:t>
  </m:r>
  <m:r>
    <m:t>d</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:r>
    <m:t>t</m:t>
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
  <m:r>
    <m:t>  </m:t>
  </m:r>
  <m:r>
    <m:t>u</m:t>
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
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>k</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>p</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
      <m:r>
        <m:t>e</m:t>
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
            <m:t>z</m:t>
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
        <m:t>−</m:t>
      </m:r>
      <m:r>
        <m:t>v</m:t>
      </m:r>
    </m:num>
    <m:den>
      <m:acc>
        <m:accPr>
          <m:chr m:val="̂"/>
        </m:accPr>
        <m:e>
          <m:r>
            <m:t>b</m:t>
          </m:r>
        </m:e>
      </m:acc>
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
  <m:r>
    <m:t>e</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>=</m:t>
  </m:r>
  <m:r>
    <m:t>r</m:t>
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
        <m:t>z</m:t>
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

### ② ESO 观测器

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:sSub>
    <m:e>
      <m:acc>
        <m:accPr>
          <m:chr m:val="̇"/>
        </m:accPr>
        <m:e>
          <m:r>
            <m:t>z</m:t>
          </m:r>
        </m:e>
      </m:acc>
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
    <m:t>=</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>z</m:t>
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
    <m:t>+</m:t>
  </m:r>
  <m:acc>
    <m:accPr>
      <m:chr m:val="̂"/>
    </m:accPr>
    <m:e>
      <m:r>
        <m:t>b</m:t>
      </m:r>
    </m:e>
  </m:acc>
  <m:r>
    <m:t>u</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>+</m:t>
  </m:r>
  <m:r>
    <m:t>v</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>+</m:t>
  </m:r>
  <m:r>
    <m:t>2</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>ω</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>o</m:t>
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
    <m:t>x</m:t>
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
        <m:t>z</m:t>
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
    <m:t>)</m:t>
  </m:r>
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
      <m:acc>
        <m:accPr>
          <m:chr m:val="̇"/>
        </m:accPr>
        <m:e>
          <m:r>
            <m:t>z</m:t>
          </m:r>
        </m:e>
      </m:acc>
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
  <m:sSubSup>
    <m:e>
      <m:r>
        <m:t>ω</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>o</m:t>
      </m:r>
    </m:sub>
    <m:sup>
      <m:r>
        <m:t>2</m:t>
      </m:r>
    </m:sup>
  </m:sSubSup>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:r>
    <m:t>x</m:t>
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
        <m:t>z</m:t>
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
    <m:t>)</m:t>
  </m:r>
</m:oMath>
```

### ③ 重复通道

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:r>
    <m:t>v</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:r>
    <m:t>t</m:t>
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
  <m:r>
    <m:t>Q</m:t>
  </m:r>
  <m:r>
    <m:t> </m:t>
  </m:r>
  <m:r>
    <m:t>v</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:r>
    <m:t>t</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>−</m:t>
  </m:r>
  <m:r>
    <m:t>T</m:t>
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
  <m:r>
    <m:t>φ</m:t>
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
        <m:t>e</m:t>
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
    <m:t>)</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>,</m:t>
  </m:r>
  <m:r>
    <m:t>  </m:t>
  </m:r>
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
    <m:t>(</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>e</m:t>
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
    <m:t>)</m:t>
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
    <m:t>κ</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>|</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>e</m:t>
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
    <m:t>|</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>,</m:t>
  </m:r>
  <m:r>
    <m:t>  </m:t>
  </m:r>
  <m:r>
    <m:t>T</m:t>
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
        <m:t>g</m:t>
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
    <m:t>1</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>+</m:t>
  </m:r>
  <m:r>
    <m:t>δ</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>)</m:t>
  </m:r>
</m:oMath>
```

### ④ 外部输入能量

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:r>
    <m:t>W</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:r>
    <m:t>t</m:t>
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
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>|</m:t>
  </m:r>
  <m:r>
    <m:t>d</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:r>
    <m:t>t</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>)</m:t>
  </m:r>
  <m:sSup>
    <m:e>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>|</m:t>
      </m:r>
    </m:e>
    <m:sup>
      <m:r>
        <m:t>2</m:t>
      </m:r>
    </m:sup>
  </m:sSup>
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
    <m:t>|</m:t>
  </m:r>
  <m:acc>
    <m:accPr>
      <m:chr m:val="̇"/>
    </m:accPr>
    <m:e>
      <m:r>
        <m:t>r</m:t>
      </m:r>
    </m:e>
  </m:acc>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:r>
    <m:t>t</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>)</m:t>
  </m:r>
  <m:sSup>
    <m:e>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>|</m:t>
      </m:r>
    </m:e>
    <m:sup>
      <m:r>
        <m:t>2</m:t>
      </m:r>
    </m:sup>
  </m:sSup>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>,</m:t>
  </m:r>
  <m:r>
    <m:t>  </m:t>
  </m:r>
  <m:acc>
    <m:accPr>
      <m:chr m:val="‾"/>
    </m:accPr>
    <m:e>
      <m:r>
        <m:t>W</m:t>
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
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>sup</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>t</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:t>W</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:r>
    <m:t>t</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>)</m:t>
  </m:r>
</m:oMath>
```

## D.2 假设

### ⑤ A2：律D 增益盒

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>k</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>p</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>,</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>e</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>f</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>f</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>∈</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>[</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>k</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>p</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>,</m:t>
  </m:r>
  <m:r>
    <m:t> </m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>k</m:t>
      </m:r>
    </m:e>
    <m:sub>
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
    <m:t>1</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>+</m:t>
  </m:r>
  <m:r>
    <m:t>a</m:t>
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
    <m:t>]</m:t>
  </m:r>
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
        <m:t>ω</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>o</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>,</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>e</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>f</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>f</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>∈</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>[</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>ω</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>o</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>,</m:t>
  </m:r>
  <m:r>
    <m:t> </m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>ω</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>o</m:t>
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
    <m:t>1</m:t>
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
        <m:t>b</m:t>
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
    <m:t>]</m:t>
  </m:r>
</m:oMath>
```

### ⑥ A3：律J 参数盒与速率

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:acc>
    <m:accPr>
      <m:chr m:val="̂"/>
    </m:accPr>
    <m:e>
      <m:r>
        <m:t>b</m:t>
      </m:r>
    </m:e>
  </m:acc>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:r>
    <m:t>t</m:t>
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
    <m:t>∈</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>[</m:t>
  </m:r>
  <m:bar>
    <m:barPr>
      <m:pos m:val="bot"/>
    </m:barPr>
    <m:e>
      <m:r>
        <m:t>b</m:t>
      </m:r>
    </m:e>
  </m:bar>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>,</m:t>
  </m:r>
  <m:r>
    <m:t> </m:t>
  </m:r>
  <m:bar>
    <m:barPr>
      <m:pos m:val="top"/>
    </m:barPr>
    <m:e>
      <m:r>
        <m:t>b</m:t>
      </m:r>
    </m:e>
  </m:bar>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>]</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>,</m:t>
  </m:r>
  <m:r>
    <m:t>  </m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>|</m:t>
  </m:r>
  <m:acc>
    <m:accPr>
      <m:chr m:val="̇"/>
    </m:accPr>
    <m:e>
      <m:acc>
        <m:accPr>
          <m:chr m:val="̂"/>
        </m:accPr>
        <m:e>
          <m:r>
            <m:t>b</m:t>
          </m:r>
        </m:e>
      </m:acc>
    </m:e>
  </m:acc>
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
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>L</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>J</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
</m:oMath>
```

### ⑦ A4：律T 参数盒

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>|</m:t>
  </m:r>
  <m:acc>
    <m:accPr>
      <m:chr m:val="̂"/>
    </m:accPr>
    <m:e>
      <m:r>
        <m:t>δ</m:t>
      </m:r>
    </m:e>
  </m:acc>
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
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>δ</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>max</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>,</m:t>
  </m:r>
  <m:r>
    <m:t>  </m:t>
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
    <m:t>Δ</m:t>
  </m:r>
  <m:acc>
    <m:accPr>
      <m:chr m:val="̂"/>
    </m:accPr>
    <m:e>
      <m:r>
        <m:t>δ</m:t>
      </m:r>
    </m:e>
  </m:acc>
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
    <m:t>σ</m:t>
  </m:r>
</m:oMath>
```

### ⑧ A5：盒内一致 ISS

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:acc>
    <m:accPr>
      <m:chr m:val="̇"/>
    </m:accPr>
    <m:e>
      <m:r>
        <m:t>V</m:t>
      </m:r>
    </m:e>
  </m:acc>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>≤</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>−</m:t>
  </m:r>
  <m:r>
    <m:t>α</m:t>
  </m:r>
  <m:r>
    <m:t>V</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>+</m:t>
  </m:r>
  <m:r>
    <m:t>β</m:t>
  </m:r>
  <m:r>
    <m:t>W</m:t>
  </m:r>
</m:oMath>
```

### ⑨ A6：参数灵敏度界

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
            <m:t>V</m:t>
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
    </m:e>
  </m:d>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>≤</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>c</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>V</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
</m:oMath>
```

## D.2.1 假设 A5 的证明

### ⑩ 消去 u 后的 z1 方程

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:sSub>
    <m:e>
      <m:acc>
        <m:accPr>
          <m:chr m:val="̇"/>
        </m:accPr>
        <m:e>
          <m:r>
            <m:t>z</m:t>
          </m:r>
        </m:e>
      </m:acc>
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
    <m:t>=</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>k</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>p</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:t>e</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>+</m:t>
  </m:r>
  <m:r>
    <m:t>2</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>ω</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>o</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>e</m:t>
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

### ⑪ e 的方程

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:acc>
    <m:accPr>
      <m:chr m:val="̇"/>
    </m:accPr>
    <m:e>
      <m:r>
        <m:t>e</m:t>
      </m:r>
    </m:e>
  </m:acc>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>=</m:t>
  </m:r>
  <m:acc>
    <m:accPr>
      <m:chr m:val="̇"/>
    </m:accPr>
    <m:e>
      <m:r>
        <m:t>r</m:t>
      </m:r>
    </m:e>
  </m:acc>
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
        <m:t>p</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:t>e</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>−</m:t>
  </m:r>
  <m:r>
    <m:t>2</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>ω</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>o</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>e</m:t>
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

### ⑫ e1 的方程

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:sSub>
    <m:e>
      <m:acc>
        <m:accPr>
          <m:chr m:val="̇"/>
        </m:accPr>
        <m:e>
          <m:r>
            <m:t>e</m:t>
          </m:r>
        </m:e>
      </m:acc>
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
    <m:t>=</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:r>
    <m:t>ρ</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>−</m:t>
  </m:r>
  <m:r>
    <m:t>1</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>)</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>k</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>p</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:t>e</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>−</m:t>
  </m:r>
  <m:r>
    <m:t>2</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>ω</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>o</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>e</m:t>
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
    <m:t>−</m:t>
  </m:r>
  <m:r>
    <m:t>ρ</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>z</m:t>
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
    <m:t>−</m:t>
  </m:r>
  <m:r>
    <m:t>ρ</m:t>
  </m:r>
  <m:r>
    <m:t>v</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>+</m:t>
  </m:r>
  <m:r>
    <m:t>d</m:t>
  </m:r>
</m:oMath>
```

### ⑬ z2 的方程

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:sSub>
    <m:e>
      <m:acc>
        <m:accPr>
          <m:chr m:val="̇"/>
        </m:accPr>
        <m:e>
          <m:r>
            <m:t>z</m:t>
          </m:r>
        </m:e>
      </m:acc>
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
  <m:sSubSup>
    <m:e>
      <m:r>
        <m:t>ω</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>o</m:t>
      </m:r>
    </m:sub>
    <m:sup>
      <m:r>
        <m:t>2</m:t>
      </m:r>
    </m:sup>
  </m:sSubSup>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>e</m:t>
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

### ⑭ 三阶矩阵 M

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:r>
    <m:t>M</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>=</m:t>
  </m:r>
  <m:d>
    <m:dPr>
      <m:begChr m:val="["/>
      <m:sepChr m:val=""/>
      <m:endChr m:val="]"/>
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
                <m:mcJc m:val="center"/>
                <m:count m:val="1"/>
              </m:mcPr>
            </m:mc>
            <m:mc>
              <m:mcPr>
                <m:mcJc m:val="center"/>
                <m:count m:val="1"/>
              </m:mcPr>
            </m:mc>
            <m:mc>
              <m:mcPr>
                <m:mcJc m:val="center"/>
                <m:count m:val="1"/>
              </m:mcPr>
            </m:mc>
          </m:mcs>
        </m:mPr>
        <m:mr>
          <m:e>
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
                  <m:t>p</m:t>
                </m:r>
              </m:sub>
            </m:sSub>
          </m:e>
          <m:e>
            <m:r>
              <m:rPr>
                <m:sty m:val="p"/>
              </m:rPr>
              <m:t>−</m:t>
            </m:r>
            <m:r>
              <m:t>2</m:t>
            </m:r>
            <m:sSub>
              <m:e>
                <m:r>
                  <m:t>ω</m:t>
                </m:r>
              </m:e>
              <m:sub>
                <m:r>
                  <m:t>o</m:t>
                </m:r>
              </m:sub>
            </m:sSub>
          </m:e>
          <m:e>
            <m:r>
              <m:t>0</m:t>
            </m:r>
          </m:e>
        </m:mr>
        <m:mr>
          <m:e>
            <m:r>
              <m:rPr>
                <m:sty m:val="p"/>
              </m:rPr>
              <m:t>(</m:t>
            </m:r>
            <m:r>
              <m:t>ρ</m:t>
            </m:r>
            <m:r>
              <m:rPr>
                <m:sty m:val="p"/>
              </m:rPr>
              <m:t>−</m:t>
            </m:r>
            <m:r>
              <m:t>1</m:t>
            </m:r>
            <m:r>
              <m:rPr>
                <m:sty m:val="p"/>
              </m:rPr>
              <m:t>)</m:t>
            </m:r>
            <m:sSub>
              <m:e>
                <m:r>
                  <m:t>k</m:t>
                </m:r>
              </m:e>
              <m:sub>
                <m:r>
                  <m:t>p</m:t>
                </m:r>
              </m:sub>
            </m:sSub>
          </m:e>
          <m:e>
            <m:r>
              <m:rPr>
                <m:sty m:val="p"/>
              </m:rPr>
              <m:t>−</m:t>
            </m:r>
            <m:r>
              <m:t>2</m:t>
            </m:r>
            <m:sSub>
              <m:e>
                <m:r>
                  <m:t>ω</m:t>
                </m:r>
              </m:e>
              <m:sub>
                <m:r>
                  <m:t>o</m:t>
                </m:r>
              </m:sub>
            </m:sSub>
          </m:e>
          <m:e>
            <m:r>
              <m:rPr>
                <m:sty m:val="p"/>
              </m:rPr>
              <m:t>−</m:t>
            </m:r>
            <m:r>
              <m:t>ρ</m:t>
            </m:r>
          </m:e>
        </m:mr>
        <m:mr>
          <m:e>
            <m:r>
              <m:t>0</m:t>
            </m:r>
          </m:e>
          <m:e>
            <m:sSubSup>
              <m:e>
                <m:r>
                  <m:t>ω</m:t>
                </m:r>
              </m:e>
              <m:sub>
                <m:r>
                  <m:t>o</m:t>
                </m:r>
              </m:sub>
              <m:sup>
                <m:r>
                  <m:t>2</m:t>
                </m:r>
              </m:sup>
            </m:sSubSup>
          </m:e>
          <m:e>
            <m:r>
              <m:t>0</m:t>
            </m:r>
          </m:e>
        </m:mr>
      </m:m>
    </m:e>
  </m:d>
</m:oMath>
```

### ⑮ 特征多项式 p(s)

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:r>
    <m:t>p</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:r>
    <m:t>s</m:t>
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
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>det</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:r>
    <m:t>s</m:t>
  </m:r>
  <m:r>
    <m:t>I</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>−</m:t>
  </m:r>
  <m:r>
    <m:t>M</m:t>
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
  <m:sSup>
    <m:e>
      <m:r>
        <m:t>s</m:t>
      </m:r>
    </m:e>
    <m:sup>
      <m:r>
        <m:t>3</m:t>
      </m:r>
    </m:sup>
  </m:sSup>
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
  <m:r>
    <m:t>2</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>ω</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>o</m:t>
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
        <m:t>p</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>)</m:t>
  </m:r>
  <m:sSup>
    <m:e>
      <m:r>
        <m:t>s</m:t>
      </m:r>
    </m:e>
    <m:sup>
      <m:r>
        <m:t>2</m:t>
      </m:r>
    </m:sup>
  </m:sSup>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>+</m:t>
  </m:r>
  <m:r>
    <m:t>ρ</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>ω</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>o</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>ω</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>o</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>+</m:t>
  </m:r>
  <m:r>
    <m:t>2</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>k</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>p</m:t>
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
    <m:t>s</m:t>
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
        <m:t>p</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:t>ρ</m:t>
  </m:r>
  <m:sSubSup>
    <m:e>
      <m:r>
        <m:t>ω</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>o</m:t>
      </m:r>
    </m:sub>
    <m:sup>
      <m:r>
        <m:t>2</m:t>
      </m:r>
    </m:sup>
  </m:sSubSup>
</m:oMath>
```

### ⑯ Routh–Hurwitz 余量

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
        <m:t>1</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>a</m:t>
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
    <m:t>−</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>a</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>3</m:t>
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
    <m:t>2</m:t>
  </m:r>
  <m:r>
    <m:t>ρ</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>ω</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>o</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>ω</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>o</m:t>
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
        <m:t>)</m:t>
      </m:r>
    </m:e>
    <m:sup>
      <m:r>
        <m:t>2</m:t>
      </m:r>
    </m:sup>
  </m:sSup>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>&gt;</m:t>
  </m:r>
  <m:r>
    <m:t>0</m:t>
  </m:r>
</m:oMath>
```

### ⑰ Lyapunov 方程

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:sSup>
    <m:e>
      <m:r>
        <m:t>A</m:t>
      </m:r>
    </m:e>
    <m:sup>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>⊤</m:t>
      </m:r>
    </m:sup>
  </m:sSup>
  <m:r>
    <m:t>P</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>+</m:t>
  </m:r>
  <m:r>
    <m:t>P</m:t>
  </m:r>
  <m:r>
    <m:t>A</m:t>
  </m:r>
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
    <m:t>I</m:t>
  </m:r>
</m:oMath>
```

### ⑱ V0 的导数不等式

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:sSub>
    <m:e>
      <m:acc>
        <m:accPr>
          <m:chr m:val="̇"/>
        </m:accPr>
        <m:e>
          <m:r>
            <m:t>V</m:t>
          </m:r>
        </m:e>
      </m:acc>
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
    <m:t>≤</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>−</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>∥</m:t>
  </m:r>
  <m:r>
    <m:t>ξ</m:t>
  </m:r>
  <m:sSup>
    <m:e>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∥</m:t>
      </m:r>
    </m:e>
    <m:sup>
      <m:r>
        <m:t>2</m:t>
      </m:r>
    </m:sup>
  </m:sSup>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>+</m:t>
  </m:r>
  <m:r>
    <m:t>2</m:t>
  </m:r>
  <m:sSup>
    <m:e>
      <m:r>
        <m:t>ξ</m:t>
      </m:r>
    </m:e>
    <m:sup>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>⊤</m:t>
      </m:r>
    </m:sup>
  </m:sSup>
  <m:r>
    <m:t>P</m:t>
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
            <m:t>B</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>v</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
      <m:r>
        <m:t>v</m:t>
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
            <m:t>B</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>d</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
      <m:r>
        <m:t>d</m:t>
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
            <m:t>B</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>r</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
      <m:acc>
        <m:accPr>
          <m:chr m:val="̇"/>
        </m:accPr>
        <m:e>
          <m:r>
            <m:t>r</m:t>
          </m:r>
        </m:e>
      </m:acc>
    </m:e>
  </m:d>
</m:oMath>
```

### ⑲ 指数稳定界 ||e^{At}||

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>∥</m:t>
  </m:r>
  <m:sSup>
    <m:e>
      <m:r>
        <m:t>e</m:t>
      </m:r>
    </m:e>
    <m:sup>
      <m:r>
        <m:t>A</m:t>
      </m:r>
      <m:r>
        <m:t>t</m:t>
      </m:r>
    </m:sup>
  </m:sSup>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>∥</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>≤</m:t>
  </m:r>
  <m:r>
    <m:t>K</m:t>
  </m:r>
  <m:sSup>
    <m:e>
      <m:r>
        <m:t>e</m:t>
      </m:r>
    </m:e>
    <m:sup>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>−</m:t>
      </m:r>
      <m:r>
        <m:t>μ</m:t>
      </m:r>
      <m:r>
        <m:t>t</m:t>
      </m:r>
    </m:sup>
  </m:sSup>
</m:oMath>
```

### ⑳ 零状态解

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>e</m:t>
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
    <m:t>(</m:t>
  </m:r>
  <m:r>
    <m:t>t</m:t>
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
  <m:r>
    <m:t>C</m:t>
  </m:r>
  <m:nary>
    <m:naryPr>
      <m:chr m:val="∫"/>
      <m:limLoc m:val="subSup"/>
      <m:subHide m:val="off"/>
      <m:supHide m:val="off"/>
    </m:naryPr>
    <m:sub>
      <m:r>
        <m:t>0</m:t>
      </m:r>
    </m:sub>
    <m:sup>
      <m:r>
        <m:t>t</m:t>
      </m:r>
    </m:sup>
    <m:e>
      <m:sSup>
        <m:e>
          <m:r>
            <m:t>e</m:t>
          </m:r>
        </m:e>
        <m:sup>
          <m:r>
            <m:t>A</m:t>
          </m:r>
          <m:r>
            <m:rPr>
              <m:sty m:val="p"/>
            </m:rPr>
            <m:t>(</m:t>
          </m:r>
          <m:r>
            <m:t>t</m:t>
          </m:r>
          <m:r>
            <m:rPr>
              <m:sty m:val="p"/>
            </m:rPr>
            <m:t>−</m:t>
          </m:r>
          <m:r>
            <m:t>s</m:t>
          </m:r>
          <m:r>
            <m:rPr>
              <m:sty m:val="p"/>
            </m:rPr>
            <m:t>)</m:t>
          </m:r>
        </m:sup>
      </m:sSup>
    </m:e>
  </m:nary>
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
            <m:t>B</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>v</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
      <m:r>
        <m:t>v</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>(</m:t>
      </m:r>
      <m:r>
        <m:t>s</m:t>
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
            <m:t>B</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>d</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
      <m:r>
        <m:t>d</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>(</m:t>
      </m:r>
      <m:r>
        <m:t>s</m:t>
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
            <m:t>B</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>r</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
      <m:acc>
        <m:accPr>
          <m:chr m:val="̇"/>
        </m:accPr>
        <m:e>
          <m:r>
            <m:t>r</m:t>
          </m:r>
        </m:e>
      </m:acc>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>(</m:t>
      </m:r>
      <m:r>
        <m:t>s</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>)</m:t>
      </m:r>
    </m:e>
  </m:d>
  <m:r>
    <m:t>d</m:t>
  </m:r>
  <m:r>
    <m:t>s</m:t>
  </m:r>
</m:oMath>
```

### ㉑ L∞ 增益不等式

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>∥</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>e</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>1</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:sSub>
    <m:e>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∥</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∞</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>≤</m:t>
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
        <m:t>∥</m:t>
      </m:r>
      <m:r>
        <m:t>C</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∥</m:t>
      </m:r>
      <m:r>
        <m:t>K</m:t>
      </m:r>
    </m:num>
    <m:den>
      <m:r>
        <m:t>μ</m:t>
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
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∥</m:t>
      </m:r>
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>B</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>v</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∥</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∥</m:t>
      </m:r>
      <m:r>
        <m:t>v</m:t>
      </m:r>
      <m:sSub>
        <m:e>
          <m:r>
            <m:rPr>
              <m:sty m:val="p"/>
            </m:rPr>
            <m:t>∥</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:rPr>
              <m:sty m:val="p"/>
            </m:rPr>
            <m:t>∞</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
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
        <m:t>∥</m:t>
      </m:r>
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>B</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>d</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∥</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∥</m:t>
      </m:r>
      <m:r>
        <m:t>d</m:t>
      </m:r>
      <m:sSub>
        <m:e>
          <m:r>
            <m:rPr>
              <m:sty m:val="p"/>
            </m:rPr>
            <m:t>∥</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:rPr>
              <m:sty m:val="p"/>
            </m:rPr>
            <m:t>∞</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
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
        <m:t>∥</m:t>
      </m:r>
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>B</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>r</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∥</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∥</m:t>
      </m:r>
      <m:acc>
        <m:accPr>
          <m:chr m:val="̇"/>
        </m:accPr>
        <m:e>
          <m:r>
            <m:t>r</m:t>
          </m:r>
        </m:e>
      </m:acc>
      <m:sSub>
        <m:e>
          <m:r>
            <m:rPr>
              <m:sty m:val="p"/>
            </m:rPr>
            <m:t>∥</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:rPr>
              <m:sty m:val="p"/>
            </m:rPr>
            <m:t>∞</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
    </m:e>
  </m:d>
</m:oMath>
```

### ㉒ c_v, c_d, c_r 的定义

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
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
        <m:t>∥</m:t>
      </m:r>
      <m:r>
        <m:t>C</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∥</m:t>
      </m:r>
      <m:r>
        <m:t>K</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∥</m:t>
      </m:r>
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>B</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>v</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∥</m:t>
      </m:r>
    </m:num>
    <m:den>
      <m:r>
        <m:t>μ</m:t>
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
        <m:t>c</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>d</m:t>
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
        <m:t>∥</m:t>
      </m:r>
      <m:r>
        <m:t>C</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∥</m:t>
      </m:r>
      <m:r>
        <m:t>K</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∥</m:t>
      </m:r>
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>B</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>d</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∥</m:t>
      </m:r>
    </m:num>
    <m:den>
      <m:r>
        <m:t>μ</m:t>
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
        <m:t>c</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>r</m:t>
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
        <m:t>∥</m:t>
      </m:r>
      <m:r>
        <m:t>C</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∥</m:t>
      </m:r>
      <m:r>
        <m:t>K</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∥</m:t>
      </m:r>
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>B</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>r</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∥</m:t>
      </m:r>
    </m:num>
    <m:den>
      <m:r>
        <m:t>μ</m:t>
      </m:r>
    </m:den>
  </m:f>
</m:oMath>
```

### ㉓ 合并 c_w

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>∥</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>e</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>1</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:sSub>
    <m:e>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∥</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∞</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>≤</m:t>
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
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>∥</m:t>
  </m:r>
  <m:r>
    <m:t>v</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∥</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∞</m:t>
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
        <m:t>c</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>w</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>∥</m:t>
  </m:r>
  <m:rad>
    <m:radPr>
      <m:degHide m:val="on"/>
    </m:radPr>
    <m:deg/>
    <m:e>
      <m:r>
        <m:t>W</m:t>
      </m:r>
    </m:e>
  </m:rad>
  <m:sSub>
    <m:e>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∥</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∞</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
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
        <m:t>c</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>w</m:t>
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
        <m:t>c</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>d</m:t>
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
        <m:t>c</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>r</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
</m:oMath>
```

### ㉔ RC 输出的上界

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>|</m:t>
  </m:r>
  <m:r>
    <m:t>v</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:r>
    <m:t>t</m:t>
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
    <m:t>|</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>≤</m:t>
  </m:r>
  <m:r>
    <m:t>Q</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>|</m:t>
  </m:r>
  <m:r>
    <m:t>v</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:r>
    <m:t>t</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>−</m:t>
  </m:r>
  <m:r>
    <m:t>T</m:t>
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
    <m:t>|</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>+</m:t>
  </m:r>
  <m:r>
    <m:t>κ</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>|</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>e</m:t>
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
    <m:t>(</m:t>
  </m:r>
  <m:r>
    <m:t>t</m:t>
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
    <m:t>|</m:t>
  </m:r>
  <m:r>
    <m:t> </m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>⇒</m:t>
  </m:r>
  <m:r>
    <m:t> </m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>∥</m:t>
  </m:r>
  <m:r>
    <m:t>v</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∥</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∞</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>≤</m:t>
  </m:r>
  <m:f>
    <m:fPr>
      <m:type m:val="bar"/>
    </m:fPr>
    <m:num>
      <m:r>
        <m:t>κ</m:t>
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
      <m:r>
        <m:t>Q</m:t>
      </m:r>
    </m:den>
  </m:f>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>∥</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>e</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>1</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:sSub>
    <m:e>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∥</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∞</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>≡</m:t>
  </m:r>
  <m:acc>
    <m:accPr>
      <m:chr m:val="‾"/>
    </m:accPr>
    <m:e>
      <m:r>
        <m:t>κ</m:t>
      </m:r>
    </m:e>
  </m:acc>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>∥</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>e</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>1</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:sSub>
    <m:e>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∥</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∞</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
</m:oMath>
```

### ㉕ 小增益闭合

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:d>
    <m:dPr>
      <m:begChr m:val="("/>
      <m:sepChr m:val=""/>
      <m:endChr m:val=")"/>
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
      <m:acc>
        <m:accPr>
          <m:chr m:val="‾"/>
        </m:accPr>
        <m:e>
          <m:r>
            <m:t>κ</m:t>
          </m:r>
        </m:e>
      </m:acc>
    </m:e>
  </m:d>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>∥</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>e</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>1</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:sSub>
    <m:e>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∥</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∞</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>≤</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>c</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>w</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>∥</m:t>
  </m:r>
  <m:rad>
    <m:radPr>
      <m:degHide m:val="on"/>
    </m:radPr>
    <m:deg/>
    <m:e>
      <m:r>
        <m:t>W</m:t>
      </m:r>
    </m:e>
  </m:rad>
  <m:sSub>
    <m:e>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∥</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∞</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
</m:oMath>
```

### ㉖ 合成后的 A5

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:acc>
    <m:accPr>
      <m:chr m:val="̇"/>
    </m:accPr>
    <m:e>
      <m:r>
        <m:t>V</m:t>
      </m:r>
    </m:e>
  </m:acc>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>≤</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>−</m:t>
  </m:r>
  <m:r>
    <m:t>α</m:t>
  </m:r>
  <m:r>
    <m:t>V</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>+</m:t>
  </m:r>
  <m:r>
    <m:t>β</m:t>
  </m:r>
  <m:r>
    <m:t>W</m:t>
  </m:r>
</m:oMath>
```

## D.3 引理 1（参数紧致 + 速率有界）

### ㉗ 律D：饱和门控

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:r>
    <m:t>g</m:t>
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
      <m:sSubSup>
        <m:e>
          <m:r>
            <m:t>e</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>1</m:t>
          </m:r>
          <m:r>
            <m:t>m</m:t>
          </m:r>
        </m:sub>
        <m:sup>
          <m:r>
            <m:t>2</m:t>
          </m:r>
        </m:sup>
      </m:sSubSup>
    </m:num>
    <m:den>
      <m:sSubSup>
        <m:e>
          <m:r>
            <m:t>e</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>1</m:t>
          </m:r>
          <m:r>
            <m:t>m</m:t>
          </m:r>
        </m:sub>
        <m:sup>
          <m:r>
            <m:t>2</m:t>
          </m:r>
        </m:sup>
      </m:sSubSup>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>+</m:t>
      </m:r>
      <m:sSup>
        <m:e>
          <m:r>
            <m:t>ε</m:t>
          </m:r>
        </m:e>
        <m:sup>
          <m:r>
            <m:t>2</m:t>
          </m:r>
        </m:sup>
      </m:sSup>
    </m:den>
  </m:f>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>∈</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>[</m:t>
  </m:r>
  <m:r>
    <m:t>0</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>,</m:t>
  </m:r>
  <m:r>
    <m:t>1</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>]</m:t>
  </m:r>
</m:oMath>
```

### ㉘ 律J：低通解析解

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:acc>
    <m:accPr>
      <m:chr m:val="̂"/>
    </m:accPr>
    <m:e>
      <m:r>
        <m:t>b</m:t>
      </m:r>
    </m:e>
  </m:acc>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:r>
    <m:t>t</m:t>
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
        <m:t>b</m:t>
      </m:r>
    </m:e>
    <m:sub>
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
        <m:t>o</m:t>
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
        <m:t>l</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>+</m:t>
  </m:r>
  <m:d>
    <m:dPr>
      <m:begChr m:val="("/>
      <m:sepChr m:val=""/>
      <m:endChr m:val=")"/>
      <m:grow/>
    </m:dPr>
    <m:e>
      <m:acc>
        <m:accPr>
          <m:chr m:val="̂"/>
        </m:accPr>
        <m:e>
          <m:r>
            <m:t>b</m:t>
          </m:r>
        </m:e>
      </m:acc>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>(</m:t>
      </m:r>
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>t</m:t>
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
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>−</m:t>
      </m:r>
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>b</m:t>
          </m:r>
        </m:e>
        <m:sub>
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
            <m:t>o</m:t>
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
            <m:t>l</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
    </m:e>
  </m:d>
  <m:sSup>
    <m:e>
      <m:r>
        <m:t>e</m:t>
      </m:r>
    </m:e>
    <m:sup>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>−</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>(</m:t>
      </m:r>
      <m:r>
        <m:t>t</m:t>
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
            <m:t>t</m:t>
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
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>/</m:t>
      </m:r>
      <m:r>
        <m:t>τ</m:t>
      </m:r>
    </m:sup>
  </m:sSup>
</m:oMath>
```

### ㉙ 律J：速率界

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>|</m:t>
  </m:r>
  <m:acc>
    <m:accPr>
      <m:chr m:val="̇"/>
    </m:accPr>
    <m:e>
      <m:acc>
        <m:accPr>
          <m:chr m:val="̂"/>
        </m:accPr>
        <m:e>
          <m:r>
            <m:t>b</m:t>
          </m:r>
        </m:e>
      </m:acc>
    </m:e>
  </m:acc>
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
        <m:t>|</m:t>
      </m:r>
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>b</m:t>
          </m:r>
        </m:e>
        <m:sub>
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
            <m:t>o</m:t>
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
            <m:t>l</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
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
            <m:t>b</m:t>
          </m:r>
        </m:e>
      </m:acc>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>(</m:t>
      </m:r>
      <m:r>
        <m:t>t</m:t>
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
        <m:t>|</m:t>
      </m:r>
    </m:num>
    <m:den>
      <m:r>
        <m:t>τ</m:t>
      </m:r>
    </m:den>
  </m:f>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>≤</m:t>
  </m:r>
  <m:f>
    <m:fPr>
      <m:type m:val="bar"/>
    </m:fPr>
    <m:num>
      <m:bar>
        <m:barPr>
          <m:pos m:val="top"/>
        </m:barPr>
        <m:e>
          <m:r>
            <m:t>b</m:t>
          </m:r>
        </m:e>
      </m:bar>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>−</m:t>
      </m:r>
      <m:bar>
        <m:barPr>
          <m:pos m:val="bot"/>
        </m:barPr>
        <m:e>
          <m:r>
            <m:t>b</m:t>
          </m:r>
        </m:e>
      </m:bar>
    </m:num>
    <m:den>
      <m:r>
        <m:t>τ</m:t>
      </m:r>
    </m:den>
  </m:f>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>=</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>L</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>J</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
</m:oMath>
```

### ㉚ 律T：抖动后的 δ 界

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:r>
    <m:t>δ</m:t>
  </m:r>
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
        <m:t>δ</m:t>
      </m:r>
    </m:e>
  </m:acc>
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
    <m:t>Δ</m:t>
  </m:r>
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
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>ω</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>d</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:t>t</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>)</m:t>
  </m:r>
  <m:r>
    <m:t> </m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>⇒</m:t>
  </m:r>
  <m:r>
    <m:t> </m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>|</m:t>
  </m:r>
  <m:r>
    <m:t>δ</m:t>
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
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>δ</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>max</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
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
    <m:t>Δ</m:t>
  </m:r>
</m:oMath>
```

### ㉛ 律T：时滞紧致区间

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:r>
    <m:t>T</m:t>
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
        <m:t>g</m:t>
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
    <m:t>1</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>+</m:t>
  </m:r>
  <m:r>
    <m:t>δ</m:t>
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
    <m:t>∈</m:t>
  </m:r>
  <m:d>
    <m:dPr>
      <m:begChr m:val="["/>
      <m:sepChr m:val=""/>
      <m:endChr m:val="]"/>
      <m:grow/>
    </m:dPr>
    <m:e>
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
        </m:sub>
      </m:sSub>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>(</m:t>
      </m:r>
      <m:r>
        <m:t>1</m:t>
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
            <m:t>δ</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:rPr>
              <m:sty m:val="p"/>
            </m:rPr>
            <m:t>max</m:t>
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
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>Δ</m:t>
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
      <m:r>
        <m:t> </m:t>
      </m:r>
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
        </m:sub>
      </m:sSub>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>(</m:t>
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
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>δ</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:rPr>
              <m:sty m:val="p"/>
            </m:rPr>
            <m:t>max</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
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
        <m:t>Δ</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>)</m:t>
      </m:r>
    </m:e>
  </m:d>
</m:oMath>
```

### ㉜ 总速率上界 L

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:r>
    <m:t>L</m:t>
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
        <m:t>L</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>J</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
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
      <m:r>
        <m:t>σ</m:t>
      </m:r>
    </m:num>
    <m:den>
      <m:r>
        <m:t>N</m:t>
      </m:r>
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>P</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>d</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
    </m:den>
  </m:f>
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
      <m:r>
        <m:t>2</m:t>
      </m:r>
      <m:r>
        <m:t>π</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>Δ</m:t>
      </m:r>
    </m:num>
    <m:den>
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>P</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>d</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
    </m:den>
  </m:f>
</m:oMath>
```

## D.4 引理 2（慢变参数 Lyapunov 界）

### ㉝ 引理 2 结论

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:r>
    <m:t>V</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:r>
    <m:t>t</m:t>
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
    <m:t>≤</m:t>
  </m:r>
  <m:sSup>
    <m:e>
      <m:r>
        <m:t>e</m:t>
      </m:r>
    </m:e>
    <m:sup>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>−</m:t>
      </m:r>
      <m:r>
        <m:t>α</m:t>
      </m:r>
      <m:r>
        <m:t>t</m:t>
      </m:r>
    </m:sup>
  </m:sSup>
  <m:r>
    <m:t>V</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:r>
    <m:t>0</m:t>
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
  <m:f>
    <m:fPr>
      <m:type m:val="bar"/>
    </m:fPr>
    <m:num>
      <m:r>
        <m:t>β</m:t>
      </m:r>
      <m:acc>
        <m:accPr>
          <m:chr m:val="‾"/>
        </m:accPr>
        <m:e>
          <m:r>
            <m:t>W</m:t>
          </m:r>
        </m:e>
      </m:acc>
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
            <m:t>V</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
      <m:r>
        <m:t>L</m:t>
      </m:r>
    </m:num>
    <m:den>
      <m:r>
        <m:t>α</m:t>
      </m:r>
    </m:den>
  </m:f>
</m:oMath>
```

### ㉞ 链式法则不等式

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:acc>
    <m:accPr>
      <m:chr m:val="̇"/>
    </m:accPr>
    <m:e>
      <m:r>
        <m:t>V</m:t>
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
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∇</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>x</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:t>V</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>⋅</m:t>
  </m:r>
  <m:r>
    <m:t>f</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:r>
    <m:t>x</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>,</m:t>
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
        <m:t>V</m:t>
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
  <m:acc>
    <m:accPr>
      <m:chr m:val="̇"/>
    </m:accPr>
    <m:e>
      <m:r>
        <m:t>θ</m:t>
      </m:r>
    </m:e>
  </m:acc>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>≤</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>−</m:t>
  </m:r>
  <m:r>
    <m:t>α</m:t>
  </m:r>
  <m:r>
    <m:t>V</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>+</m:t>
  </m:r>
  <m:r>
    <m:t>β</m:t>
  </m:r>
  <m:r>
    <m:t>W</m:t>
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
        <m:t>c</m:t>
      </m:r>
    </m:e>
    <m:sub>
      <m:r>
        <m:t>V</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:t>L</m:t>
  </m:r>
</m:oMath>
```

### ㉟ Gronwall 积分

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:r>
    <m:t>V</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:r>
    <m:t>t</m:t>
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
    <m:t>≤</m:t>
  </m:r>
  <m:sSup>
    <m:e>
      <m:r>
        <m:t>e</m:t>
      </m:r>
    </m:e>
    <m:sup>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>−</m:t>
      </m:r>
      <m:r>
        <m:t>α</m:t>
      </m:r>
      <m:r>
        <m:t>t</m:t>
      </m:r>
    </m:sup>
  </m:sSup>
  <m:r>
    <m:t>V</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:r>
    <m:t>0</m:t>
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
  <m:d>
    <m:dPr>
      <m:begChr m:val="("/>
      <m:sepChr m:val=""/>
      <m:endChr m:val=")"/>
      <m:grow/>
    </m:dPr>
    <m:e>
      <m:r>
        <m:t>β</m:t>
      </m:r>
      <m:acc>
        <m:accPr>
          <m:chr m:val="‾"/>
        </m:accPr>
        <m:e>
          <m:r>
            <m:t>W</m:t>
          </m:r>
        </m:e>
      </m:acc>
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
            <m:t>V</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
      <m:r>
        <m:t>L</m:t>
      </m:r>
    </m:e>
  </m:d>
  <m:f>
    <m:fPr>
      <m:type m:val="bar"/>
    </m:fPr>
    <m:num>
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
            <m:t>e</m:t>
          </m:r>
        </m:e>
        <m:sup>
          <m:r>
            <m:rPr>
              <m:sty m:val="p"/>
            </m:rPr>
            <m:t>−</m:t>
          </m:r>
          <m:r>
            <m:t>α</m:t>
          </m:r>
          <m:r>
            <m:t>t</m:t>
          </m:r>
        </m:sup>
      </m:sSup>
    </m:num>
    <m:den>
      <m:r>
        <m:t>α</m:t>
      </m:r>
    </m:den>
  </m:f>
</m:oMath>
```

## D.5 定理（三律联立有界性）

### ㊱ 定理：误差界

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>|</m:t>
  </m:r>
  <m:r>
    <m:t>e</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:r>
    <m:t>t</m:t>
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
    <m:t>|</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>≤</m:t>
  </m:r>
  <m:rad>
    <m:radPr>
      <m:degHide m:val="on"/>
    </m:radPr>
    <m:deg/>
    <m:e>
      <m:f>
        <m:fPr>
          <m:type m:val="bar"/>
        </m:fPr>
        <m:num>
          <m:r>
            <m:t>β</m:t>
          </m:r>
          <m:acc>
            <m:accPr>
              <m:chr m:val="‾"/>
            </m:accPr>
            <m:e>
              <m:r>
                <m:t>W</m:t>
              </m:r>
            </m:e>
          </m:acc>
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
                <m:t>V</m:t>
              </m:r>
            </m:sub>
          </m:sSub>
          <m:r>
            <m:t>L</m:t>
          </m:r>
        </m:num>
        <m:den>
          <m:r>
            <m:t>α</m:t>
          </m:r>
          <m:sSub>
            <m:e>
              <m:r>
                <m:t>c</m:t>
              </m:r>
            </m:e>
            <m:sub>
              <m:r>
                <m:t>0</m:t>
              </m:r>
            </m:sub>
          </m:sSub>
        </m:den>
      </m:f>
    </m:e>
  </m:rad>
</m:oMath>
```

### ㊲ 第 2 步：V 的上界

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:limLow>
    <m:e>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>sup</m:t>
      </m:r>
    </m:e>
    <m:lim>
      <m:r>
        <m:t>t</m:t>
      </m:r>
    </m:lim>
  </m:limLow>
  <m:r>
    <m:t>V</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
  </m:r>
  <m:r>
    <m:t>t</m:t>
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
    <m:t>≤</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>max</m:t>
  </m:r>
  <m:d>
    <m:dPr>
      <m:begChr m:val="{"/>
      <m:sepChr m:val=""/>
      <m:endChr m:val="}"/>
      <m:grow/>
    </m:dPr>
    <m:e>
      <m:r>
        <m:t>V</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>(</m:t>
      </m:r>
      <m:r>
        <m:t>0</m:t>
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
      <m:r>
        <m:t> </m:t>
      </m:r>
      <m:f>
        <m:fPr>
          <m:type m:val="bar"/>
        </m:fPr>
        <m:num>
          <m:r>
            <m:t>β</m:t>
          </m:r>
          <m:acc>
            <m:accPr>
              <m:chr m:val="‾"/>
            </m:accPr>
            <m:e>
              <m:r>
                <m:t>W</m:t>
              </m:r>
            </m:e>
          </m:acc>
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
                <m:t>V</m:t>
              </m:r>
            </m:sub>
          </m:sSub>
          <m:r>
            <m:t>L</m:t>
          </m:r>
        </m:num>
        <m:den>
          <m:r>
            <m:t>α</m:t>
          </m:r>
        </m:den>
      </m:f>
    </m:e>
  </m:d>
</m:oMath>
```

## D.6 注记

### ㊳ A5 的可检验形式（小增益）

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:sSub>
    <m:e>
      <m:r>
        <m:t>γ</m:t>
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
    <m:t>=</m:t>
  </m:r>
  <m:sSub>
    <m:e>
      <m:d>
        <m:dPr>
          <m:begChr m:val="∥"/>
          <m:sepChr m:val=""/>
          <m:endChr m:val="∥"/>
          <m:grow/>
        </m:dPr>
        <m:e>
          <m:r>
            <m:t>Q</m:t>
          </m:r>
          <m:r>
            <m:t> </m:t>
          </m:r>
          <m:sSup>
            <m:e>
              <m:r>
                <m:t>e</m:t>
              </m:r>
            </m:e>
            <m:sup>
              <m:r>
                <m:rPr>
                  <m:sty m:val="p"/>
                </m:rPr>
                <m:t>−</m:t>
              </m:r>
              <m:r>
                <m:t>s</m:t>
              </m:r>
              <m:r>
                <m:t>T</m:t>
              </m:r>
            </m:sup>
          </m:sSup>
          <m:sSub>
            <m:e>
              <m:r>
                <m:t>S</m:t>
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
            <m:t>(</m:t>
          </m:r>
          <m:r>
            <m:t>s</m:t>
          </m:r>
          <m:r>
            <m:rPr>
              <m:sty m:val="p"/>
            </m:rPr>
            <m:t>)</m:t>
          </m:r>
        </m:e>
      </m:d>
    </m:e>
    <m:sub>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>∞</m:t>
      </m:r>
    </m:sub>
  </m:sSub>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>&lt;</m:t>
  </m:r>
  <m:r>
    <m:t>1</m:t>
  </m:r>
</m:oMath>
```

---

说明：LaTeX 源在 _appxD_math.md，docx 由 pandoc 生成，OMML 已清理命名空间。