def get_secret_patterns():
    return {
        "AWS Access Key": r"AKIA[0-9A-Z]{16}",
        "AWS Secret Key": r"(?i)aws(.{0,20})?(secret|key)['\"]?[:=][ \"]?([A-Za-z0-9/+=]{40})",
        "Generic API Key": r"(?i)(api|token|key)['\"]?[:=][ \"]?['\"]?[A-Za-z0-9_\-]{16,45}['\"]?",
        "Private Key": r"-----BEGIN PRIVATE KEY-----",
        "Slack Token": r"xox[baprs]-([0-9a-zA-Z]{10,48})",
        "GitHub Token": r"ghp_[A-Za-z0-9_]{36}",
        "Password Keyword": r"(?i)(password|passwd)['\"]?[:=][ \"]?.+"
    }
