# 附录 D：律 D / J / T 的稳定性与有界性（OMML 片段）

> 与报告附录 D 正文一致，共 15 个式子。
> 用法：打开同目录「附录D_三律稳定性_公式.docx」复制整条公式；或复制下面的 m:oMath 片段。
> 符号：b0/hat b、kp、ω_o、Q、T=Tg(1+δ)、σ、Δ、δmax、τ、α、β、L_J、S0(s)。

## D.1 模型与假设

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
  <m:r>
    <m:t>x</m:t>
  </m:r>
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
    <m:t>Q</m:t>
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
    <m:t>&lt;</m:t>
  </m:r>
  <m:r>
    <m:t>1</m:t>
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
</m:oMath>
```

### ④ 小增益条件

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

### ⑤ ISS-Lyapunov 不等式

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
        <m:t>|</m:t>
      </m:r>
      <m:r>
        <m:t>d</m:t>
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
    </m:e>
  </m:d>
</m:oMath>
```

## D.2 律D：增益盒紧致

### ⑥ 检测量门控

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

### ⑦ 等效增益上下界

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
    <m:t>=</m:t>
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

## D.3 律J：参数紧致与慢变

### ⑧ 限幅更新（α=1）

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:sSup>
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
    <m:sup>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>+</m:t>
      </m:r>
    </m:sup>
  </m:sSup>
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
    <m:t>c</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>l</m:t>
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
    <m:t>p</m:t>
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
        <m:t>+</m:t>
      </m:r>
      <m:r>
        <m:t>α</m:t>
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
                <m:t>b</m:t>
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
                <m:t>e</m:t>
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
                <m:t>s</m:t>
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
        </m:e>
      </m:d>
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
    </m:e>
  </m:d>
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
    <m:t>α</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>=</m:t>
  </m:r>
  <m:r>
    <m:t>1</m:t>
  </m:r>
</m:oMath>
```

### ⑨ 低通切换与速率界

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
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
    </m:num>
    <m:den>
      <m:r>
        <m:t>τ</m:t>
      </m:r>
    </m:den>
  </m:f>
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
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>(</m:t>
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
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>)</m:t>
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
        <m:t>t</m:t>
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
    <m:t>≡</m:t>
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

### ⑩ 环路增益比区间

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:r>
    <m:t>ρ</m:t>
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
            <m:t>b</m:t>
          </m:r>
        </m:e>
        <m:sub>
          <m:r>
            <m:t>0</m:t>
          </m:r>
        </m:sub>
      </m:sSub>
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
      <m:f>
        <m:fPr>
          <m:type m:val="bar"/>
        </m:fPr>
        <m:num>
          <m:sSub>
            <m:e>
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
            </m:e>
            <m:sub>
              <m:r>
                <m:t>0</m:t>
              </m:r>
            </m:sub>
          </m:sSub>
        </m:num>
        <m:den>
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
        </m:den>
      </m:f>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>,</m:t>
      </m:r>
      <m:r>
        <m:t> </m:t>
      </m:r>
      <m:f>
        <m:fPr>
          <m:type m:val="bar"/>
        </m:fPr>
        <m:num>
          <m:sSub>
            <m:e>
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
            </m:e>
            <m:sub>
              <m:r>
                <m:t>0</m:t>
              </m:r>
            </m:sub>
          </m:sSub>
        </m:num>
        <m:den>
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
        </m:den>
      </m:f>
    </m:e>
  </m:d>
</m:oMath>
```

## D.4 律T：限幅与慢变

### ⑪ 搜索更新律

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:sSup>
    <m:e>
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
    </m:e>
    <m:sup>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>+</m:t>
      </m:r>
    </m:sup>
  </m:sSup>
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
    <m:t>c</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>l</m:t>
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
    <m:t>p</m:t>
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
            <m:t>δ</m:t>
          </m:r>
        </m:e>
      </m:acc>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>−</m:t>
      </m:r>
      <m:r>
        <m:t>σ</m:t>
      </m:r>
      <m:r>
        <m:t> </m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>s</m:t>
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
        <m:t>n</m:t>
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
            <m:t>I</m:t>
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
        <m:t>,</m:t>
      </m:r>
      <m:r>
        <m:t> </m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>±</m:t>
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
    </m:e>
  </m:d>
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

### ⑫ 叠加抖动后的周期修正

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

### ⑬ 时滞区间

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

## D.5 定理与证明

### ⑭ 闭环有界性

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
        <m:t>|</m:t>
      </m:r>
      <m:r>
        <m:t>x</m:t>
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
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>|</m:t>
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
        <m:t>|</m:t>
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
        <m:t>|</m:t>
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
        <m:t>|</m:t>
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
        <m:t>|</m:t>
      </m:r>
      <m:r>
        <m:t>v</m:t>
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
        <m:t>|</m:t>
      </m:r>
    </m:e>
  </m:d>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>≤</m:t>
  </m:r>
  <m:r>
    <m:t>C</m:t>
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
          <m:chr m:val="‾"/>
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
        <m:t>,</m:t>
      </m:r>
      <m:acc>
        <m:accPr>
          <m:chr m:val="‾"/>
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
        <m:t>,</m:t>
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
        <m:t>,</m:t>
      </m:r>
      <m:r>
        <m:t>σ</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>,</m:t>
      </m:r>
      <m:r>
        <m:t>κ</m:t>
      </m:r>
      <m:r>
        <m:rPr>
          <m:sty m:val="p"/>
        </m:rPr>
        <m:t>,</m:t>
      </m:r>
      <m:sSub>
        <m:e>
          <m:r>
            <m:t>η</m:t>
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
</m:oMath>
```

### ⑮ 残差界

```xml
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:r>
    <m:t>x</m:t>
  </m:r>
  <m:r>
    <m:t> </m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>→</m:t>
  </m:r>
  <m:r>
    <m:t> </m:t>
  </m:r>
  <m:r>
    <m:t>r</m:t>
  </m:r>
  <m:r>
    <m:rPr>
      <m:sty m:val="p"/>
    </m:rPr>
    <m:t>+</m:t>
  </m:r>
  <m:r>
    <m:t>O</m:t>
  </m:r>
  <m:d>
    <m:dPr>
      <m:begChr m:val="("/>
      <m:sepChr m:val=""/>
      <m:endChr m:val=")"/>
      <m:grow/>
    </m:dPr>
    <m:e>
      <m:f>
        <m:fPr>
          <m:type m:val="bar"/>
        </m:fPr>
        <m:num>
          <m:acc>
            <m:accPr>
              <m:chr m:val="‾"/>
            </m:accPr>
            <m:e>
              <m:r>
                <m:t>d</m:t>
              </m:r>
            </m:e>
          </m:acc>
        </m:num>
        <m:den>
          <m:r>
            <m:t>α</m:t>
          </m:r>
        </m:den>
      </m:f>
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
        <m:t>+</m:t>
      </m:r>
      <m:r>
        <m:t>σ</m:t>
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
        </m:num>
        <m:den>
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
        </m:den>
      </m:f>
    </m:e>
  </m:d>
</m:oMath>
```

---

说明：LaTeX 源在 _appxD_math.md，docx 由 pandoc 生成，OMML 已清理命名空间；MathType 可直接识别 docx 里的公式。