#! /usr/bin/env python
# -*- coding: utf-8 -*-
import random



string='QuXAv1SKKpPqk6YqrsmizUiJCo12BYd2dQ6Pc65DUpwvDz6Km2vYdKuYRlXvdurFl7UMJOTy8hjfd9zHicBUMSEVSlcSaApmxJU8mbS2IT6FrLGPpzwBSVVICKIstuGbnZ7UWsP1R8ZbATz6jKRI6sk5PrNDGCff36SIoDiz2tFBcbXV2oHUI9KPpEpMEZpsWihrN7a1f9sn9xUy0F7WvplJxDmQ0RsAiu6u6aoI4Xh4UUyVPOxU78Xzp2wJh1flmat4w1NQQmQG6Po4BV4aZbFW2b0jJJrPXSIR6Wk8InLOQeG5T4UeJMk7bar7DbfGajZkqZlSYh2Emm92bWhFJvdiIlLLRR3X1eCJYmDxvEBfOnf6LjpsYp8Ca1CjfpqwWMKnXPYjPXp3sCZuVr4yT59wfJobCUNvbBzA8lX1q5qOuTIbZElK12NpGxMslvcZOptxoUoBJUC0CG1gqULun3bUnp1KzRiwdScakzHC7pGL1pAYYKmUBcPH3l1aiCmBdZrL4FtMFduocruyzCW09IMWdkilJlnydOm5ja60ebZopNnFZBCBXQdaFtmkS1vMC273Z13UTXoMCaK2YF3uJkONjr7oR2LDbQyBxYX35Wr1qigEnjEhAMZZOB3QMK3uCQsqFZFXk9NsTh9aiCnmhoaQWAqsNIO62olXehTbQEsuFd8WaPD74wlJDQA2OF7AJWY1dBYAYBeq30GQuwF4kbczI4FUrKlxeTVO8rQAxHJsBoM8UZgrlO6jkqsNfBWja1yZdjpPoqCKIJm68DIiwy4l9RV87xFOjk4QRJvnRZjl8LGWERNi1107BDeQZTAjEMe79yLqQqMrFhVygUj2CVnD2WEyNQZwnOKBrQobLAgitRa6LhM5sFyshPncFSJZsaiNpFkwrYlKo0zLTLqRof5Dqc00UetBUTf7SVZswKVds3JfTk40twshheLskQdHds9dpCJyjG4yE00uytSw2SixZBkIcIVUXWvJNx1TPh7cHHcCbAKLguYRV3Gp8OFm'

for i in range(883):
    num = random.randint(0,900)
    password = string[num:num+15]
    email = string[num+20:num+32] + '@qq.com'
    print "update user_dis set password = '%s',email='%s' where id=%s;" % (password,email.lower(),i+1)
