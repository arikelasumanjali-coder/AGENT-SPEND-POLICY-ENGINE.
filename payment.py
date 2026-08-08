from fastapi import HTTPException


def verify_payment(payment_status):

    if payment_status != "PAID":

        raise HTTPException(
            status_code=402,
            detail="Payment Required"
        )


    return True