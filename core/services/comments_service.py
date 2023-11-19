from dataclasses import asdict

from core.gateways.abstract_gateway import AbstractGateway
from core.gateways.comment_gateway import (CommentGateway, 
                                            comment_gateway)

from core import aliases
from core.models import Comment
from core.schemas import CommentScheme
from core.utils import markdown_to_html


class CommentService:
    model: Comment = Comment
    
    def __init__(self, 
                 gateway: CommentGateway
                 ) -> None:
        self.gateway = gateway
        
    def create_comment(self, 
                       comment: CommentScheme
                      ) -> None:
        model = self.model(**asdict(comment))
        model.text = markdown_to_html(
            model.text
        )
        self.gateway.create(model)

        return
    
    def get_comments(self, 
                     post_key: aliases.PostKey):
        return self.gateway.filter_by(post_key=post_key)
        

comment_service = CommentService(gateway=comment_gateway)