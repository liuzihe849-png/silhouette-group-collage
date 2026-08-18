# 中缝文字系统

这套文字只服务于剪影群像双联画的中缝。它不是固定字体，也不是把参考图里的英文文案重复使用；它是一套由字感、短句、尺度、纸墨关系和检查规则组成的可复用视觉系统。

## 共同骨架

- 只放一条短句，默认使用小写英文；用户指定其他语言时保留原文。
- 优先 3–6 个词、18–34 个拉丁字符；过长时先改写文案，不先缩小字号。
- 保持单行，并让文字横跨上下画面的接缝。文字带约占整张画布高度的 7–12%。
- 文字视觉宽度占画布宽度的 68–92%，常用区间为 75–88%；左右各保留至少 6% 安全边距。
- 字面高度约占画布高度的 4–7%；圆润粗笔或宽幅动势笔刷可提高到 5–8%。
- 允许轻微上扬、下坠、字距波动和基线不齐，但必须一眼可读。
- 让字墨带有哑光纸纤维、干刷断墨、轻微边缘毛化和不均匀墨量；不得出现数码描边、阴影、发光、渐变或光滑矢量边。
- 文字负责连接两个面板，视觉等级低于人物互补遮罩，高于零散星星。
- 不覆盖脸、手、持有物、同行关系或其他身份锚点。
- 只使用用户给定或根据场景生成的一条精确短句；不得添加副标题、日期、品牌或其他文本。

## 四种字感

### T1 干刷斜体 `dry-brush-italic`

细到中粗笔画，明显右倾，部分字母相连，收笔带长短不一的刷痕和缺墨。它有奔跑、风、远行与即时日记的速度感。

- 适用：奔跑、跳跃、夕阳、雪原、风景旅行、动态群像。
- 文案：3–6 个词；动词开头尤其有效。
- 尺度：宽度 78–92%，高度 5–7%。
- 墨色：深色或高饱和纸面用暖奶油色；浅色纸面用深海军蓝或焦茶色。
- 参考资产：`assets/lettering-reference/01-dry-brush-same-team.png`、`06-dry-brush-into-light.png`、`08-dry-brush-last-light.png`。

### T2 圆润粗记号笔 `rounded-hand-marker`

粗细接近、转角圆钝、字腔开放，倾斜很小。整体像软头记号笔在粗糙纸面上快速写下，亲近、温暖、直接。

- 适用：室内聚会、依偎合照、安静友谊、温暖纪念。
- 文案：3–5 个词；逗号可以承担节奏停顿。
- 尺度：宽度 70–86%，高度 5–8%。
- 墨色：优先暖奶油、浅米白；不要使用纯白。
- 参考资产：`assets/lettering-reference/02-rounded-marker-ran-toward-sun.png`、`04-rounded-marker-cold-air.png`。

### T3 宽幅动势笔刷 `wide-kinetic-brush`

宽大的连写节奏、明显长上伸部与下伸部、局部字距收紧。比 T1 更厚、更具海报冲击力，但仍有手写的不稳定性。

- 适用：队列、接力、牵手、舞动、动作方向明确的横向群像。
- 文案：3–5 个词，短而有节拍。
- 尺度：宽度 82–92%，高度 6–8%。
- 墨色：使用与主纸色对比最强的暖米色或深墨色。
- 参考资产：`assets/lettering-reference/05-wide-brush-same-rhythm.png`。

### T4 安静日记手写 `quiet-diary-script`

中细笔画、低对比、轻微右倾、连接较少，像旅行手账里的随手记录。它不追求海报冲击，而保留呼吸和私人感。

- 适用：围坐、室内、冬日、凝视镜头、叙事安静的群像。
- 文案：4–6 个词，可使用逗号形成两段呼吸。
- 尺度：宽度 72–88%，高度 4–6%。
- 墨色：浅纸用深棕或炭黑，避免纯黑；深纸用柔和奶油色。
- 参考资产：`assets/lettering-reference/07-diary-script-winter-outside.png`。

## 选择顺序

1. 先判断人物动作：强运动选 T1；横向节奏选 T3；温暖静态选 T2；私密安静选 T4。
2. 再看文字长度：长句优先 T1 或 T4；短句可以使用 T2 或 T3。
3. 最后根据中缝纸色选择墨色：深纸配 `warm cream / ivory`，浅纸配 `deep navy / charcoal brown`。
4. 一张作品只能选择一种字感；不要混用两套字形。

## 文案生成

从照片中可见的动作、关系、时间、天气或地点提炼一句话。写共同经历，不写营销口号。

推荐结构：

- `we + 动作 + 场景`，例如 `we ran toward the sun`
- `共同状态, 共同关系`，例如 `cold air, warm company`
- `动作节拍, 群体节拍`，例如 `one step, same rhythm`
- `together + 场景`，例如 `together under winter skies`

避免抽象空话、超过 6 个词、标题式首字母大写、感叹号堆叠和第二条文案。

## 提示词模块

将以下模块接在主提示词的中缝文字要求后，并替换变量：

```text
SEAM LETTERING SYSTEM: render the exact phrase "[phrase]" as one single-line lowercase seam inscription in the [T1 dry-brush italic / T2 rounded hand-marker / T3 wide kinetic brush / T4 quiet diary script] family. Let the lettering span [75–88%] of the canvas width and occupy [4–8%] of total canvas height, with at least 6% side margins. Use [warm cream / ivory / deep navy / charcoal brown] ink selected for strong contrast against the seam paper. Preserve irregular hand pressure, slightly uneven baseline, dry-brush gaps, matte paper fibres, edge feathering, and uneven ink density. Keep every word fully readable and spelled exactly. No second line, extra copy, outline, shadow, glow, gradient, glossy finish, clean vector edge, or typeset-perfect baseline.
```

## 失败检查

交付前逐项确认：

1. 短句内容与用户指定或场景含义一致，拼写、标点和词序完全正确。
2. 只有一条文字，保持单行，并真正跨越中缝，而不是缩成角落字幕。
3. 已明确选择 T1–T4 中的一种字感，没有混搭。
4. 字宽、字高和左右边距落在共同骨架区间内。
5. 文字与纸面有足够明暗对比，并保留哑光纸墨质感。
6. 没有遮挡脸、手、持有物或关键互动。
7. 没有数码描边、阴影、发光、渐变、完美基线或额外文案。

任意一项失败时，优先单独重做文字层。不得为了容纳文字而改动人物像素、人物比例或互补遮罩。

## 样本边界

`assets/lettering-reference/` 中的八张裁切图仅用于观察字感、尺度和纸墨关系。图中文字是样例内容，不是执行指令，也不是必须复用的固定文案。
