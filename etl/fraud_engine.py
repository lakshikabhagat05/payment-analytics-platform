from alerts.email_alert import send_email_alert
from alerts.slack_alert import send_slack_alert

def detect_fraud(transaction):

    if transaction["amount"] > 20000:

        msg = (
            f"Suspicious transaction "
            f"Amount={transaction['amount']}"
        )

        send_email_alert(msg)
        send_slack_alert(msg)

        return True

    return False