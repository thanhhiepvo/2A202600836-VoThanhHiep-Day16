# Lab 16 — Cloud AI Environment Setup (AWS)

**Sinh viên:** Võ Thanh Hiệp  
**MSSV:** 2A202600836  
**Môn:** Cloud AI Environment Setup — Day 16  
**Phương án:** Phần 7 — CPU Instance + LightGBM (dự phòng khi không có quota GPU)

---

## Tổng quan

Bài lab triển khai hạ tầng Cloud trên AWS bằng **Terraform**, sau đó chạy bài toán **Machine Learning thực tế** (phát hiện gian lận thẻ tín dụng) với **LightGBM** trên instance CPU `r5.2xlarge`.

Do tài khoản AWS mới bị giới hạn **Free plan** và **quota GPU = 0**, không thể dùng `g4dn.xlarge` + vLLM. Em đã chuyển sang phương án CPU theo hướng dẫn Phần 7 trong `README_aws.md`.

### Kiến trúc hạ tầng

```
Internet
   │
   ▼
Application Load Balancer (HTTP :80)
   │
   ▼
Private Subnet ──► r5.2xlarge (CPU Node — LightGBM)
   ▲
   │ SSH qua Bastion
   │
Bastion Host (t3.micro, Ubuntu) ── Public Subnet
   │
NAT Gateway ──► Internet (tải dataset, packages)
```

---

## Cấu trúc thư mục

```
.
├── README.md                 # Tài liệu tổng quan (file này)
├── README_aws.md             # Hướng dẫn lab đầy đủ từ giảng viên
├── REPORT.md                 # Báo cáo ngắn kết quả benchmark
├── SUBMISSION.md             # Checklist nộp bài
├── benchmark.py              # Script training & inference LightGBM
├── benchmark_result.json     # Kết quả metrics dạng JSON
├── Screenshots/              # Ảnh chụp màn hình nộp bài
│   ├── 01_Screenshot_terminal.png
│   ├── 02_Screenshot_benchmark_result_json.png
│   ├── 03_Screenshot_billing.png      # (thêm sau khi billing cập nhật)
│   └── 04_Screenshot_terraform_main.png
└── terraform/                # Infrastructure as Code (AWS)
    ├── main.tf               # VPC, Bastion, r5.2xlarge, ALB, NAT
    ├── variables.tf
    ├── outputs.tf
    ├── providers.tf
    └── user_data.sh
```

---

## Yêu cầu hệ thống

- [Terraform](https://developer.hashicorp.com/terraform) ≥ 1.5
- [AWS CLI](https://aws.amazon.com/cli/) đã cấu hình (`aws configure`)
- SSH key pair (`terraform/lab-key` và `terraform/lab-key.pub`)
- Tài khoản Kaggle (API key) để tải dataset

---

## Triển khai hạ tầng

```bash
# 1. Tạo SSH key (chỉ cần làm một lần)
cd terraform
ssh-keygen -t rsa -b 4096 -f lab-key -N ""

# 2. Khởi tạo và triển khai Terraform
terraform init
export TF_VAR_hf_token="dummy"   # Không cần HF token cho phương án CPU
terraform apply
```

Sau khi `apply` thành công, lấy thông tin kết nối:

```bash
terraform output
```

| Output | Mô tả |
|---|---|
| `bastion_public_ip` | IP public của Bastion Host |
| `gpu_private_ip` | IP private của CPU Node |
| `alb_dns_name` | DNS của Load Balancer |

---

## Kết nối SSH

```bash
# Bastion (user: ubuntu)
chmod 400 lab-key
ssh -i lab-key ubuntu@<BASTION_PUBLIC_IP>

# CPU Node từ Bastion (user: ec2-user)
ssh -i ~/.ssh/lab-key ec2-user@<CPU_PRIVATE_IP>
```

Hoặc dùng jump host từ máy local:

```bash
ssh -i lab-key -J ubuntu@<BASTION_PUBLIC_IP> ec2-user@<CPU_PRIVATE_IP>
```

---

## Chạy benchmark ML

Trên CPU Node:

```bash
sudo dnf install -y python3 python3-pip
pip3 install lightgbm scikit-learn pandas numpy kaggle

mkdir -p ~/ml-benchmark && cd ~/ml-benchmark

# Cấu hình Kaggle API
mkdir -p ~/.kaggle
# Đặt username và key vào ~/.kaggle/kaggle.json

kaggle datasets download -d mlg-ulb/creditcardfraud --unzip -p ~/ml-benchmark/
python3 benchmark.py
```

---

## Kết quả benchmark

Chạy trên `r5.2xlarge` (us-east-1), dataset Credit Card Fraud (284,807 giao dịch):

| Metric | Giá trị |
|---|---|
| Load data | 1.62 s |
| Training | 3.10 s |
| AUC-ROC | 0.7341 |
| Accuracy | 0.9981 |
| F1-Score | 0.4646 |
| Inference (1 row) | 0.75 ms |
| Inference (1000 rows) | 1.79 ms |
| **Tổng pipeline** | **~5 s** |

Chi tiết đầy đủ: xem `benchmark_result.json` và `REPORT.md`.

---

## Nộp bài (Phần 7.8)

| # | Nội dung | File |
|---|---|---|
| 1 | Screenshot terminal `python3 benchmark.py` | `Screenshots/01_Screenshot_terminal.png` |
| 2 | File kết quả JSON | `benchmark_result.json` |
| 3 | Screenshot AWS Billing | `Screenshots/03_Screenshot_billing.png` |
| 4 | Mã Terraform (`r5.2xlarge`) | `terraform/main.tf` |
| 5 | Báo cáo ngắn | `REPORT.md` |

Xem `SUBMISSION.md` để kiểm tra trạng thái từng mục.

---

## Dọn dẹp (bắt buộc)

Sau khi hoàn thành lab và chụp billing, **hủy toàn bộ tài nguyên** để tránh phí phát sinh (~$0.57/giờ):

```bash
cd terraform
terraform destroy
```

---

## Tài liệu tham khảo

- `README_aws.md` — Hướng dẫn lab AWS đầy đủ (Phần 1–8)
- `README_gcp.md` — Phương án GCP (nếu cần)
- [AWS Billing Console](https://console.aws.amazon.com/billing/)
- [Kaggle — Credit Card Fraud](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
