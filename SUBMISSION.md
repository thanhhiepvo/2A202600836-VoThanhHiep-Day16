# Danh sách nộp bài — Phần 7.8 (CPU + LightGBM)

| # | Yêu cầu | File / vị trí | Trạng thái |
|---|---|---|---|
| 1 | Screenshot terminal chạy `python3 benchmark.py` | `Screenshots/01_Screenshot_terminal.png` | ✅ |
| 2 | File `benchmark_result.json` | `benchmark_result.json` | ✅ |
| 3 | Screenshot AWS Billing (EC2 + NAT Gateway) | `Screenshots/03_Screenshot_billing.png` | ⏳ Chờ AWS cập nhật billing |
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
│   ├── 03_Screenshot_billing.png        # Thêm sau khi billing hiện EC2/NAT (mục 3)
│   └── 04_Screenshot_terraform_main.png # main.tf với r5.2xlarge (mục 4)
├── terraform/
│   └── main.tf                        # Hạ tầng đã chỉnh sửa (mục 4)
└── README_aws.md
```

## Việc cần làm thêm

1. **Billing:** Đợi ≥ 1 giờ sau `terraform apply`, vào [AWS Billing](https://console.aws.amazon.com/billing/) → **Charges by service**, chụp màn hình khi thấy **EC2** và **NAT Gateway**, lưu vào `Screenshots/03_Screenshot_billing.png`.
2. **Dọn dẹp:** Sau khi chụp billing, chạy `terraform destroy` để tránh phí phát sinh thêm.
