# Generated by Django 5.0.3 on 2025-01-02 12:23

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("is_tool_owner", models.BooleanField(db_index=True, default=False)),
                ("phone_number", models.CharField(blank=True, max_length=15)),
                ("address", models.TextField(blank=True)),
                ("verified", models.BooleanField(db_index=True, default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=100)),
                ("description", models.TextField(blank=True)),
            ],
            options={
                "indexes": [
                    models.Index(fields=["name"], name="main_catego_name_5111b9_idx")
                ],
            },
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message", models.TextField()),
                ("is_read", models.BooleanField(db_index=True, default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PromotionalCampaign",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=100)),
                ("description", models.TextField()),
                (
                    "discount_percentage",
                    models.DecimalField(db_index=True, decimal_places=2, max_digits=5),
                ),
                ("start_date", models.DateTimeField(db_index=True)),
                ("end_date", models.DateTimeField(db_index=True)),
                ("is_active", models.BooleanField(db_index=True, default=True)),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["start_date", "end_date"],
                        name="main_promot_start_d_a10191_idx",
                    ),
                    models.Index(
                        fields=["discount_percentage", "is_active"],
                        name="main_promot_discoun_8ac1f4_idx",
                    ),
                    models.Index(
                        fields=["is_active", "start_date", "end_date"],
                        name="main_promot_is_acti_39d7b8_idx",
                    ),
                ],
            },
        ),
        migrations.CreateModel(
            name="Rental",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_date", models.DateTimeField(db_index=True)),
                ("end_date", models.DateTimeField(db_index=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("approved", "Approved"),
                            ("ongoing", "Ongoing"),
                            ("completed", "Completed"),
                            ("cancelled", "Cancelled"),
                        ],
                        db_index=True,
                        default="pending",
                        max_length=20,
                    ),
                ),
                (
                    "total_cost",
                    models.DecimalField(db_index=True, decimal_places=2, max_digits=8),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "renter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rentals",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Insurance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("policy_number", models.CharField(max_length=100, unique=True)),
                (
                    "coverage_amount",
                    models.DecimalField(db_index=True, decimal_places=2, max_digits=8),
                ),
                ("premium", models.DecimalField(decimal_places=2, max_digits=6)),
                ("start_date", models.DateTimeField(db_index=True)),
                ("end_date", models.DateTimeField(db_index=True)),
                (
                    "rental",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="main.rental"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Dispute",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("description", models.TextField()),
                ("status", models.CharField(db_index=True, max_length=20)),
                ("resolution", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "resolved_at",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                (
                    "initiator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "rental",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.rental"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "rating",
                    models.PositiveIntegerField(
                        db_index=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5),
                        ],
                    ),
                ),
                ("comment", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "rental",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="main.rental"
                    ),
                ),
                (
                    "reviewer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Tool",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=200)),
                ("description", models.TextField()),
                (
                    "hourly_rate",
                    models.DecimalField(db_index=True, decimal_places=2, max_digits=6),
                ),
                ("daily_rate", models.DecimalField(decimal_places=2, max_digits=6)),
                ("weekly_rate", models.DecimalField(decimal_places=2, max_digits=6)),
                ("availability", models.BooleanField(db_index=True, default=True)),
                ("condition", models.CharField(db_index=True, max_length=50)),
                ("location", models.CharField(db_index=True, max_length=200)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="main.category",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tools",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="rental",
            name="tool",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="main.tool"
            ),
        ),
        migrations.CreateModel(
            name="Maintenance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("description", models.TextField()),
                ("date", models.DateTimeField(db_index=True)),
                (
                    "cost",
                    models.DecimalField(db_index=True, decimal_places=2, max_digits=8),
                ),
                ("performed_by", models.CharField(max_length=100)),
                (
                    "tool",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.tool"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ToolImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="tool_images/")),
                ("is_primary", models.BooleanField(default=False)),
                (
                    "tool",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="main.tool",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(db_index=True, decimal_places=2, max_digits=8),
                ),
                ("commission", models.DecimalField(decimal_places=2, max_digits=6)),
                ("status", models.CharField(db_index=True, max_length=20)),
                ("payment_method", models.CharField(db_index=True, max_length=50)),
                ("transaction_id", models.CharField(max_length=100, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "rental",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="main.rental"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserPreferences",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "max_rental_distance",
                    models.IntegerField(help_text="Maximum distance in km"),
                ),
                ("receive_promotions", models.BooleanField(default=True)),
                ("preferred_categories", models.ManyToManyField(to="main.category")),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserVerification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("document_type", models.CharField(max_length=50)),
                ("document_number", models.CharField(max_length=50)),
                ("verified_at", models.DateTimeField(blank=True, null=True)),
                ("status", models.CharField(db_index=True, max_length=20)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddIndex(
            model_name="user",
            index=models.Index(
                fields=["username"], name="main_user_usernam_b7ac05_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="user",
            index=models.Index(fields=["email"], name="main_user_email_6be720_idx"),
        ),
        migrations.AddIndex(
            model_name="user",
            index=models.Index(
                fields=["is_tool_owner", "verified"],
                name="main_user_is_tool_3984d2_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="notification",
            index=models.Index(
                fields=["user_id", "is_read"], name="main_notifi_user_id_844422_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="notification",
            index=models.Index(
                fields=["created_at", "is_read"], name="main_notifi_created_54e250_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="insurance",
            index=models.Index(
                fields=["start_date", "end_date"], name="main_insura_start_d_fa0dcb_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="insurance",
            index=models.Index(
                fields=["coverage_amount", "rental_id"],
                name="main_insura_coverag_5f5ec4_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="dispute",
            index=models.Index(
                fields=["rental_id", "status"], name="main_disput_rental__d37530_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="dispute",
            index=models.Index(
                fields=["initiator_id", "status"], name="main_disput_initiat_12f9c9_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="dispute",
            index=models.Index(
                fields=["created_at", "status"], name="main_disput_created_45e3d3_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="dispute",
            index=models.Index(
                fields=["resolved_at", "status"], name="main_disput_resolve_6fb213_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="review",
            index=models.Index(
                fields=["rating", "created_at"], name="main_review_rating_0bae08_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="review",
            index=models.Index(
                fields=["reviewer_id", "created_at"],
                name="main_review_reviewe_265e26_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="review",
            index=models.Index(
                fields=["rental_id", "rating"], name="main_review_rental__e54585_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="tool",
            index=models.Index(
                fields=["name", "location"], name="main_tool_name_3a154b_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="tool",
            index=models.Index(
                fields=["hourly_rate", "availability"],
                name="main_tool_hourly__ad2c94_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="tool",
            index=models.Index(
                fields=["condition", "category_id"], name="main_tool_conditi_c44edd_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="tool",
            index=models.Index(
                fields=["owner_id", "created_at"], name="main_tool_owner_i_d166fc_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="tool",
            index=models.Index(
                fields=["created_at", "availability"],
                name="main_tool_created_5a7a71_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="rental",
            index=models.Index(
                fields=["start_date", "end_date"], name="main_rental_start_d_51ed0a_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="rental",
            index=models.Index(
                fields=["renter_id", "status"], name="main_rental_renter__c93a52_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="rental",
            index=models.Index(
                fields=["tool_id", "status"], name="main_rental_tool_id_0fd3bc_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="rental",
            index=models.Index(
                fields=["created_at", "status"], name="main_rental_created_fb37c8_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="rental",
            index=models.Index(
                fields=["total_cost", "status"], name="main_rental_total_c_f506e6_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="maintenance",
            index=models.Index(
                fields=["tool_id", "date"], name="main_mainte_tool_id_da476c_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="maintenance",
            index=models.Index(
                fields=["cost", "date"], name="main_mainte_cost_cc56b7_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="maintenance",
            index=models.Index(
                fields=["date", "tool_id"], name="main_mainte_date_f713e8_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="transaction",
            index=models.Index(
                fields=["rental_id", "status"], name="main_transa_rental__92cad7_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="transaction",
            index=models.Index(
                fields=["amount", "status"], name="main_transa_amount_31a819_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="transaction",
            index=models.Index(
                fields=["payment_method", "status"],
                name="main_transa_payment_75c313_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="transaction",
            index=models.Index(
                fields=["created_at", "status"], name="main_transa_created_5b7be6_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="userpreferences",
            index=models.Index(
                fields=["user_id"], name="main_userpr_user_id_e9b227_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="userverification",
            index=models.Index(
                fields=["verified_at", "status"], name="main_userve_verifie_93c7a1_idx"
            ),
        ),
    ]
