# Danh sách nộp bài — Phần 7.8 (CPU + LightGBM)

| # | Yêu cầu | File / vị trí | Trạng thái |
|---|---|---|---|
| 1 | Screenshot terminal chạy `python3 benchmark.py` | `Screenshots/01_Screenshot_terminal.png` | ✅ |
| 2 | File `benchmark_result.json` | `benchmark_result.json` | ✅ |
| 3 | Screenshot AWS Billing (Cost Explorer) | `Screenshots/03_Screenshot_billing.png` | ✅ (chi phí $0 — billing delay) |
| 4 | Mã nguồn Terraform (`r5.2xlarge`) | `terraform/main.tf` | ✅ |
| 5 | Báo cáo ngắn (5–10 dòng) | `REPORT.md` | ✅ |

## Cấu trúc thư mục

```
.
├── REPORT.md                          # Báo cáo ngắn (mục 5)
├── SUBMISSION.md                      # File này — checklist nộp bài
├── benchmark.py                       # Script benchmark LightGBM
├── benchmark_result.json              # Kết quả metrics (mục 2)
├── Screenshots/
│   ├── 01_Screenshot_terminal.png       # Output benchmark.py (mục 1)
│   ├── 02_Screenshot_benchmark_result_json.png
│   ├── 03_Screenshot_billing.png        # Cost Explorer (June 2026)
│   └── 04_Screenshot_terraform_main.png # main.tf với r5.2xlarge (mục 4)
├── terraform/
│   └── main.tf                        # Hạ tầng đã chỉnh sửa (mục 4)
└── README_aws.md
```

## Việc cần làm thêm

1. ~~**Billing:**~~ Đã chụp Cost Explorer (`03_Screenshot_billing.png`). AWS billing chưa hiện EC2/NAT do delay trên tài khoản mới — đã ghi chú trong `REPORT.md`.
2. **Dọn dẹp:** Chạy `terraform destroy` để tránh phí phát sinh thêm.
