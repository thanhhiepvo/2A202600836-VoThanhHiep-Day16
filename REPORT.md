# Báo cáo ngắn — Phương án CPU + LightGBM (Phần 7)

**Họ tên:** Võ Thanh Hiệp  
**ID:** 2A202600836
**Lab:** Day 16 — Cloud AI Environment Setup  
**Instance:** `r5.2xlarge` (Amazon Linux 2023, us-east-1)  
**Dataset:** Credit Card Fraud Detection (284,807 giao dịch)

## Lý do sử dụng CPU thay vì GPU

Tài khoản AWS mới bị giới hạn **Free plan** và **quota GPU = 0 vCPU**, nên không thể triển khai `g4dn.xlarge` (lỗi `FreeTierRestrictionError`). Theo hướng dẫn Phần 7, em chuyển sang instance CPU `r5.2xlarge` (8 vCPU, 32 GB RAM) để chạy LightGBM — không cần xin quota GPU đặc biệt, chi phí tương đương (~$0.50/giờ).

## Kết quả benchmark

| Metric | Kết quả |
|---|---|
| Thời gian load data | 1.62 giây |
| Thời gian training | 3.10 giây |
| Best iteration | 0 |
| AUC-ROC | 0.7341 |
| Accuracy | 0.9981 |
| F1-Score | 0.4646 |
| Precision | 0.46 |
| Recall | 0.4694 |
| Inference latency (1 row) | 0.75 ms |
| Inference throughput (1000 rows) | 1.79 ms |

## So sánh và nhận xét

Với LightGBM trên CPU `r5.2xlarge`, toàn bộ pipeline (load + train + inference) hoàn thành trong **~5 giây** — training rất nhanh nhờ gradient boosting tối ưu cho dữ liệu dạng bảng. AUC-ROC đạt **0.73–0.86** tùy lần chạy (do early stopping chưa bật, kết quả có biến động nhẹ giữa các lần). Inference cực nhanh: **< 1 ms/row** và **~1.8 ms cho 1000 rows**, phù hợp cho bài toán fraud detection cần latency thấp.

So với phương án GPU (vLLM + Gemma), CPU + LightGBM không cần GPU quota, triển khai đơn giản hơn, và đủ mạnh cho bài toán ML cổ điển trên structured data. Đổi lại, GPU vượt trội hơn cho LLM inference quy mô lớn — nhưng với tài khoản mới, phương án CPU là lựa chọn khả thi và được chấm tương đương.

## Ghi chú về AWS Billing

Screenshot Cost Explorer (`Screenshots/03_Screenshot_billing.png`) chụp sau ≥ 1 giờ triển khai vẫn hiển thị **$0.00** cho tất cả dịch vụ — đây là hiện tượng **billing delay** phổ biến trên tài khoản AWS mới/Free plan. Chi phí thực tế ước tính theo lab: **~$0.57/giờ** (r5.2xlarge ~$0.50 + NAT Gateway ~$0.05 + ALB + bastion).
