# Excel → 网页「团队分工」自动同步流程

> 固定规则：用户每发一份新的《新西兰行程计划》Excel，按本流程更新 `index.html` 的【团队分工】并自动推送，无需再确认。

## 触发条件
用户提供一份新的行程 Excel（含【行程明细及分工】sheet）。

## 同步范围
- **仅更新【团队分工】section**（`index.html` 中 `squads` 数据）。
- 行程图、风险、打包等其他模块**不动**（除非用户另行指定）。

## 标准步骤
1. 运行解析脚本，拿到最新分工：
   ```bash
   cd nz_trip && python3 tools/parse_assign.py "<新Excel路径>"
   ```
   （依赖 `pandas`、`openpyxl`，如缺失先 `pip3 install pandas openpyxl -q`）
2. 按脚本输出的「按负责人汇总」结果，重建 `index.html` 里的 `squads` 数组：
   - 分组保持 **南岛组(sh) / 北岛组(sz) / 全员事项(all)** 三块结构。
   - 每个 duty 含 `icon / duty / owner / status / tasks`。
   - `status` 取 Excel「完成情况」原值；下拉框会自动归一到「未开始/进行中/已完成/已出票/已预订」。
3. `read_lints` 确认无错误，`preview_url` 自检渲染。
4. **自动提交并推送**（不再询问用户）：
   ```bash
   cd nz_trip && git add -A && git commit -m "按最新Excel更新团队分工" && git push origin main
   ```
5. 等 GitHub Pages 构建完成，验证线上 https://robotchancie.github.io/nz-trip/ 已更新。

## 列约定（【行程明细及分工】sheet, header 在第 1 行）
| 列序 | 含义 |
|---|---|
| 0 | 类别 |
| 1 | 关联日期 |
| 2 | 项目/事项 |
| 3 | 预定建议 |
| 4 | 负责人 |
| 5 | 完成情况 |
| 6 | 预定信息 |

## 当前负责人
emma、小夏、北北、憨憨、白菜、小颜、全员
