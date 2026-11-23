# 附录 D：律 D / J / T 的稳定性与有界性（详细版，OMML 片段）

> 详细版：每一步都标注所用假设/引理；共 21 个式子。
> 用法：打开同目录「附录D_三律稳定性_详细版.docx」复制整条公式；或复制下面的 m:oMath 片段。

## D.1 符号与模型

### ① 对象与控制律（e = r − z1）

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

### ③ 重复通道（时滞 T）

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
  <m:r>
    <m:t>r</m:t>
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
        <m:t>d</m:t>
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

## D.3 引理 1（参数紧致 + 速率有界）

### ⑩ 律D：饱和门控

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

### ⑪ 律J：低通解析解

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

### ⑫ 律J：速率界

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

### ⑬ 律T：抖动后的 δ 界

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

### ⑭ 律T：时滞紧致区间

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

### ⑮ 总速率上界 L

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

### ⑯ 引理 2 结论

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

### ⑰ 链式法则不等式

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

### ⑱ Gronwall 积分

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

### ⑲ 定理：误差界

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

### ⑳ 第 2 步：V 的上界

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

### ㉑ A5 的可检验形式（小增益）

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

说明：LaTeX 源在 _appxD_math.md，docx 由 pandoc 生成，OMML 已清理命名空间；MathType 可直接识别 docx 里的公式。