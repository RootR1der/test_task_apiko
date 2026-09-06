# Інструкція з налаштування CI/CD Pipelines та розгортання в AWS

Даний посібник містить вичерпні покрокові інструкції щодо налаштування змінних середовища для **GitLab CI** та **GitHub Actions**, конфігурації **MongoDB Atlas** та виконання розгортання через **Terraform**.

---

## 1. Налаштування бази даних (MongoDB Atlas)

1. Зареєструйтесь на [MongoDB Cloud (Atlas)](https://www.mongodb.com/cloud).
2. Створіть безкоштовний кластер (M0 Free Tier), вибравши той самий хмарний провайдер та регіон (наприклад, AWS `eu-central-1`).
3. **Database Access:**
   - Створіть користувача бази даних (наприклад, `appuser`) із надійним паролем та роллю `Read and write to any database`.
4. **Network Access:**
   - Для початкового тестування можна додати `0.0.0.0/0` (Allow Access from Anywhere).
   - Для production додайте Elastic IP вашого **AWS NAT Gateway** (його виведе Terraform у вихідних даних або його можна знайти в консолі AWS VPC -> Elastic IPs).
5. **Connection String:**
   - Натисніть **Connect** -> **Connect your application** -> виберіть Driver: Node.js.
   - Скопіюйте рядок з'єднання вигляду:
     `mongodb+srv://appuser:<password>@cluster0.abcde.mongodb.net/notes_todo?retryWrites=true&w=majority`
   - Вставте цей рядок у файл `terraform.tfvars` для змінної `database_uri`.

---

## 2. Створення IAM користувача для CI/CD в AWS

Для того, щоб GitLab або GitHub могли пушити образи в ECR та оновлювати сервіс ECS, створіть окремого користувача IAM (наприклад, `gitlab-ci-deployer`) із програмним доступом (Access keys):

### Мінімально необхідна політика (Least Privilege):
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage",
        "ecr:PutImage",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ecs:DescribeServices",
        "ecs:UpdateService",
        "ecs:DescribeTaskDefinition",
        "ecs:RegisterTaskDefinition"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "iam:PassRole"
      ],
      "Resource": "*"
    }
  ]
}
```

Збережіть згенеровані `Access Key ID` та `Secret Access Key`.

---

## 3. Налаштування змінних у GitLab CI/CD

Перейдіть у свій репозиторій на GitLab:
**Settings -> CI/CD -> Variables -> Expand -> Add variable**

Створіть наступні змінні:

| Назва змінної | Опис | Тип / Опції |
| :--- | :--- | :--- |
| `AWS_ACCESS_KEY_ID` | Access Key користувача IAM | Masked |
| `AWS_SECRET_ACCESS_KEY` | Secret Key користувача IAM | Masked |
| `AWS_ACCOUNT_ID` | 12-значний номер вашого AWS акаунту (напр. `123456789012`) | Variable |
| `AWS_DEFAULT_REGION` | Регіон AWS (напр. `eu-central-1`) | Variable |
| `ECR_REPOSITORY` | Назва ECR репозиторію (`nestjs-todo-production`) | Variable |
| `ECS_CLUSTER_NAME` | Назва ECS кластера (`nestjs-todo-production-cluster`) | Variable |
| `ECS_SERVICE_NAME` | Назва ECS сервісу (`nestjs-todo-production-service`) | Variable |

---

## 4. Налаштування Secrets у GitHub Actions (якщо використовується GitHub)

Перейдіть у свій репозиторій на GitHub:
**Settings -> Secrets and variables -> Actions -> New repository secret**

Додайте:
- `AWS_ACCESS_KEY_ID`: ваш Access Key
- `AWS_SECRET_ACCESS_KEY`: ваш Secret Access Key

---

## 5. Покроковий запуск інфраструктури через Terraform

1. Перейдіть до папки `terraform/`:
   ```bash
   cd terraform
   ```
2. Скопіюйте шаблон змінних:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```
3. Відкрийте `terraform.tfvars` та встановіть ваш реальний `database_uri` від MongoDB Atlas.
4. Ініціалізуйте Terraform:
   ```bash
   terraform init
   ```
5. Перегляньте план створення ресурсів:
   ```bash
   terraform plan
   ```
6. Застосуйте зміни (створить VPC, ALB, ECR, CloudWatch, IAM та ECS):
   ```bash
   terraform apply -auto-approve
   ```
7. Після завершення у терміналі буде виведено публічний URL:
   - `alb_dns_name`
   - `app_url` (`http://<ALB-DNS-NAME>/api`)
   - `ecr_repository_url`

---

## 6. Як працює CI/CD конвеєр

1. Розробник вносить зміни у код та робить `git push` у гілку `master` (або створює Merge Request).
2. **Етап `test`:**
   - Запускається у середовищі Node.js 18.
   - Виконує `npm ci && npm run test`.
   - **Увага:** Якщо хоча б один тест падає, виконання конвеєра негайно блокується! Стадії `build` та `deploy` не запускаються.
3. **Етап `build`:**
   - Збирає Docker-образ за допомогою multi-stage `Dockerfile`.
   - Тегує образ коротким хешем коміту (`$CI_COMMIT_SHORT_SHA`) та тагом `latest`.
   - Пушить обидва таги в приватний AWS ECR репозиторій.
4. **Етап `deploy`:**
   - Викликає `aws ecs update-service --force-new-deployment`.
   - AWS ECS Fargate піднімає нові контейнери із щойно зібраним образом.
   - Балансувальник ALB перевіряє стан нових тасок за маршрутом `/api/v1`.
   - Після успішної перевірки старі таски плавно вимикаються без жодного простою сервісу (Zero Downtime Rolling Update).
5. Ви можете відкрити `http://<ALB-DNS-NAME>/api` та перевірити роботу Swagger UI та створення нотаток у базі даних MongoDB Atlas.
