from dataclasses import asdict

from core.gateways.abstract_gateway import AbstractGateway
from core.gateways.post_gateway import (PostGateway, 
                                        post_gateway)

from core import aliases
from core.models import Post
from core.schemas import PostScheme
from core import exceptions
from core.utils import transliterate_str, markdown_to_html


class PostService:
    model: Post = Post
    
    def __init__(self, 
                 gateway: PostGateway
                 ) -> None:
        self.gateway = gateway
        
    def create_post(self, 
                    post: PostScheme
                    ) -> aliases.PostKey:
        model = self.model(**asdict(post))
        model.key = transliterate_str(post.title)
        model.text = markdown_to_html(
            model.text
        )
        self.gateway.create(model)
        
        return aliases.PostKey(model.key)
    
    def get_post(self, 
                 key: aliases.PostKey
                 ) -> Post:
        models = self.gateway.filter_by(key=key)
        
        if models:
            model = self.gateway.get(pk=models[0].pk)
            model.views += 1
            self.gateway.update(pk=model.pk, 
                                post=model)
            return model
        return
        

post_service = PostService(gateway=post_gateway)